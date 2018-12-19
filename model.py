from datetime import datetime
import peewee as pw


db = pw.SqliteDatabase('data.db')


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.now)
    updated_at = pw.DateTimeField(default=datetime.now)

    def save(self, force_insert=False, only=None):
        self.updated_at = datetime.now()
        super().save(force_insert, only)

    class Meta:
        database = db


class Video(BaseModel):
    filename = pw.CharField()


class Quality(BaseModel):
    slug = pw.CharField()
    width = pw.IntegerField()
    height = pw.IntegerField()


class VideoQuality(BaseModel):
    quality = pw.ForeignKeyField(Quality, backref="videos")
    video = pw.ForeignKeyField(Video, backref="qualities")


class WaitingQueue(BaseModel):
    video = pw.ForeignKeyField(Video, backref="wait_queue")


class ProcessedVideo(BaseModel):
    video = pw.ForeignKeyField(Video, backref="processed")
    manifest = pw.CharField()
