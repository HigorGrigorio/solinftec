# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from fastapi import Depends
from shared.infra import Controller

from config.enviroment import get_environment_variables
from .CreatePlotDTO import CreatePlotDTO
from .CreatePlotUseCase import CreatePlotUseCase

env = get_environment_variables()


class CreatePlotController(Controller):

    def __init__(self, create: CreatePlotUseCase = Depends(CreatePlotUseCase)):
        super().__init__()
        self.create = create

    async def _parse_dto(self) -> CreatePlotDTO:
        form = await self.request.form()

        if file := form.get('file'):
            filename = file.filename

            # split the filename to get the name and extension
            # e.g. filename = 'plot.png' -> name = 'plot', extension = 'png'
            # e.g. filename = 'plot' -> name = 'plot', extension = ''
            # e.g. filename = 'plot.image.jpg' -> name = 'plot.image', extension = 'png'
            name, extension = filename.rsplit('.', 1) if '.' in filename else (filename, '')

            # the description is optional
            description = form.get('description') or ''
            buffer = await file.read()

            return CreatePlotDTO(
                name=name,
                extension=extension,
                description=description,
                buffer=buffer,
                path=env.UPLOAD_PATH
            )

        raise Exception("'file' is required.")

    async def do_execute(self):
        try:
            dto = await self._parse_dto()
            result = self.create.execute(dto)

            if result.is_left:
                return self.error(result.value.error)

            return self.created({'id': result.value})
        except Exception as e:
            return self.error(e)
