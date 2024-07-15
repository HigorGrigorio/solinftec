from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import random
from datetime import datetime
import os
from qgis.core import (
    QgsProject,
    QgsLayout,
    QgsLayoutExporter,
    QgsGeometry,
    QgsApplication,
    QgsLayoutItemMap,
    QgsLayoutSize,
    QgsMapLayer,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
)
import sys
import json
from models import TalhaoMessage

def initialize_qgis():
    """
    Initializes the QGIS application and sets the necessary environment variables.

    Returns:
        QgsApplication: The initialized QGIS application instance.
    """
    qgs = QgsApplication([], False)
    qgs.initQgis()
    qgis_path = qgs.prefixPath().split("/")[0:-2]
    qgis_path = "/".join(qgis_path)
    os.environ["PATH"] = qgis_path + "\\bin" + os.pathsep + os.environ.get("PATH", "")
    return qgs


def initialize_project():
    """
    Initializes the QGIS project.

    Returns:
        QgsProject: The initialized QGIS project instance.
    """
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem(4326))
    project.setFileName("ExportingTalhao.qgs")
    add_map_layer(project)
    return project


def add_map_layer(project: QgsProject):
    """
    Adds a map layer to the QGIS project.

    Args:
        project (QgsProject): The QGIS project instance.
    """
    tmsLayer_name = "Google Satellite"
    uri = "type=xyz&zmin=0&zmax=19&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}"
    tmsLayer = QgsRasterLayer(uri, baseName=tmsLayer_name, providerType="wms")

    if not tmsLayer.isValid():
        print("Failed to load the TMS layer!")
        exit(1)
    else:
        project.addMapLayer(tmsLayer)
        print("TMS layer loaded!")


def add_talhao_layer(project: QgsProject, shapefile_path: str, layer_name: str):
    """
    Adds a talhao layer to the QGIS project.

    Args:
        project (QgsProject): The QGIS project instance.
        shapefile_path (str): The path to the shapefile.
        layer_name (str): The name of the layer.
    """
    talhaoLayer = QgsMapLayer(name=layer_name, source=shapefile_path)
    if not talhaoLayer.isValid():
        print("Failed to load the talhao layer!")
        exit(1)
    else:
        project.addMapLayer(talhaoLayer)
        print("Talhao layer loaded!")


def main():
    """
    The main function that handles the Kafka consumer and QGIS operations.
    """
    # kafka configuration
    consumer_conf = {
        "bootstrap.servers": "localhost:19092",
        "auto.offset.reset": "earliest",
        "group.id": "dionisio-group",
    }
    producer_conf = {"bootstrap.servers": "localhost:19092"}

    # consumer topic
    consumer_topic = "hera.plot-to-crops"

    # the kafka topic consumer
    consumer = Consumer(consumer_conf)

    # the kafka topic producer
    producer = Producer(producer_conf)

    running = True

    try:
        consumer.subscribe([consumer_topic])

        # initialize QGIS and project
        qgs = initialize_qgis()
        project = initialize_project()

        while running:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            # handle Error
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # end of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )

            elif msg.error():
                raise KafkaException(msg.error())
            else:
                raw = json.loads(msg.value().decode("utf-8"))
                message = TalhaoMessage(**raw)
                shapefile_path = message.shapeFilePath
                layer_name = message.layerName
                output_folder = message.outputFilePath
                coord_folder = message.coordnatesOutputPath
                add_talhao_layer(project, shapefile_path, layer_name)

                map = project.mapLayersByName("Google Satellite")[0]
                talhaoLayer = project.mapLayersByName(layer_name)[0]

                layout = QgsLayout(project)
                layout.initializeDefaults()

                map_settings = QgsLayoutExporter.ImageExportSettings()
                map_settings.dpi = 600

                polygon = QgsGeometry.fromRect(map.extent())

                exporter = QgsLayoutExporter(layout)

                for feature in talhaoLayer.getFeatures():

                    geom_intersection = QgsGeometry.intersection(
                        feature.geometry(), polygon
                    )
                    if (
                        not geom_intersection.isGeosValid()
                        or geom_intersection.isEmpty()
                    ):
                        print("Intersection is invalid or empty!")
                        continue

                    bbox = geom_intersection.boundingBox()
                    aspect_ratio = bbox.width() / bbox.height()

                    map_item = QgsLayoutItemMap.create(layout)
                    resolution = 1200
                    if aspect_ratio >= 1:
                        map_item.attemptResize(
                            QgsLayoutSize(resolution, resolution / aspect_ratio)
                        )
                    else:
                        map_item.attemptResize(
                            QgsLayoutSize(resolution * aspect_ratio, resolution)
                        )

                    map_item.setExtent(bbox)
                    map_item.setLayers([map])
                    layout.addLayoutItem(map_item)

                    # Obter coordenadas da bbox
                    xmin, ymin, xmax, ymax = (
                        bbox.xMinimum(),
                        bbox.yMinimum(),
                        bbox.xMaximum(),
                        bbox.yMaximum(),
                    )

                    # transformar coordenadas para WGS 84
                    layer_crs = talhaoLayer.crs()
                    geographic_crs = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS 84
                    transform = QgsCoordinateTransform(
                        layer_crs, geographic_crs, QgsProject.instance()
                    )
                    xmin, ymin = transform.transform(xmin, ymin)
                    xmax, ymax = transform.transform(xmax, ymax)

                    # resize layout to map size
                    map_item_size = map_item.sizeWithUnits()
                    layout.pageCollection().page(0).attemptResize(map_item_size)

                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    random_number = random.randint(
                        1000, 9999
                    )  # Gera um número aleatório entre 1000 e 9999
                    export_path = output_folder + "{}_{}_{}.png".format(
                        feature.id(), timestamp, random_number
                    )

                    exporter.layout().refresh()
                    result = exporter.exportToImage(export_path, map_settings)
                    if result == QgsLayoutExporter.Success:
                        print(f"Exported image to {export_path}")
                    else:
                        print(f"Failed to export image: {result}")

                    # Salvar coordenadas
                    coord_filename = "{}_{}_{}_coordinates.txt".format(
                        feature.id(), timestamp, random_number
                    )
                    coord_filepath = os.path.join(coord_folder, coord_filename)
                    with open(coord_filepath, "w") as coord_file:
                        coord_file.write("xmin: {}\n".format(xmin))
                        coord_file.write("ymin: {}\n".format(ymin))
                        coord_file.write("xmax: {}\n".format(xmax))
                        coord_file.write("ymax: {}\n".format(ymax))

                    layout.removeLayoutItem(map_item)

                print("Export completed successfully!")

                qgs.exitQgis()
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
