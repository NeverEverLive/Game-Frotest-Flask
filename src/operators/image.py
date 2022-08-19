from uuid import uuid4
from werkzeug.utils import secure_filename

from src.models.base_model import get_session
from src.models.image import Image
from src.schema.response import ResponseSchema
from src.schema.image import ImageSchema

def upload(image) -> ResponseSchema:
    if not image:
        return ResponseSchema(
            message="No image uploaded",
            status=False
        )
    
    filename = secure_filename(image.filename)
    mimetype = image.mimetype
    image_state = Image().fill(
        id=uuid4(),
        file=image.read(),
        name=filename,
        mimetype=mimetype
    )

    with get_session() as session:
        session.add(image_state)
        session.commit()

        return ResponseSchema(
            data=ImageSchema.from_orm(image_state),
            message="Image uploaded successfuly",
            success=True
        )
