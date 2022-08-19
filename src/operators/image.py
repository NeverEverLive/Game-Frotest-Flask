from uuid import uuid4
from werkzeug.utils import secure_filename

from src.models.base_model import get_session
from src.models.image import Image
from src.schema.response import ResponseSchema
from src.schema.image import GetImageSchema, ImageSchema

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

def get_image(image: GetImageSchema) -> ResponseSchema:
    with get_session() as session:
        genre_state = session.query(Image).filter_by(id=image.id).first()

        if not genre_state:
            return ResponseSchema(
                success=False,
                message="Same image doesn't exist"
            )

        return genre_state.file, genre_state.mimetype
