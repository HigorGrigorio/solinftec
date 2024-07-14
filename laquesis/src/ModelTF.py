import tensorflow as tf
import numpy as np


class Model:
    def __init__(self, model_path: str, model_name: str | None = None):
        self.model_path = model_path
        self.model_name = model_name
        self.model = self.load_model()

    @tf.function
    def dice_coeff(y_true, y_pred):
        smooth = 1.0
        # Flatten
        y_true_f = tf.reshape(y_true, [-1])
        y_pred_f = tf.reshape(y_pred, [-1])
        intersection = tf.reduce_sum(tf.multiply(y_true_f, y_pred_f))
        score = tf.divide(
            tf.add(tf.multiply(2.0, intersection), smooth),
            tf.add(tf.add(tf.reduce_sum(y_true_f), tf.reduce_sum(y_pred_f)), smooth),
        )
        return score

    @tf.function
    def iou(self, y_true, y_pred, smooth=1e-6):
        intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
        union = (
            tf.reduce_sum(y_true, axis=[1, 2, 3])
            + tf.reduce_sum(y_pred, axis=[1, 2, 3])
            - intersection
        )
        iou_score = tf.reduce_mean((intersection + smooth) / (union + smooth), axis=0)
        return iou_score

    @tf.function
    def iou_loss(self, y_true, y_pred):
        return 1.0 - tf.float32(self.iou(y_true, y_pred))

    def load_model(self):
        if self.model_name is None:
            return tf.keras.models.load_model(
                self.model_path,
                custom_objects={
                    "dice_coeff": self.dice_coeff,
                    "iou_loss": self.iou_loss,
                },
            )
        else:
            return tf.keras.models.load_model(
                self.model_path + self.model_name,
                custom_objects={
                    "dice_coeff": self.dice_coeff,
                    "iou_loss": self.iou_loss,
                },
            )

    def predict(self, img: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise Exception("Model not loaded")
        if not isinstance(self.model, tf.keras.Model):
            raise Exception("Model is not a tf.keras.Model")
        return self.model.predict(img)
