from datetime import datetime
import peewee as pw
from playhouse.shortcuts import dict_to_model, model_to_dict


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

    def in_queue(self):
        return len(self.wait_queue) != 0

    def is_processed(self):
        return len(self.processed) != 0

    def video_qualities(self):
        return list(set([q.quality.slug for q in self.qualities]))

    def to_dict(self):
        return model_to_dict(self, extra_attrs=['video_qualities', 'in_queue', 'is_processed'])


class Quality(BaseModel):
    slug = pw.CharField()
    width = pw.IntegerField()
    height = pw.IntegerField()

    def to_dict(self):
        return model_to_dict(self, only=Quality.slug)


class VideoQuality(BaseModel):
    quality = pw.ForeignKeyField(Quality, backref="videos")
    video = pw.ForeignKeyField(Video, backref="qualities")

    class Meta:
        db_table = 'video_quality'


class WaitingQueue(BaseModel):
    video = pw.ForeignKeyField(Video, backref="wait_queue", unique=True)

    class Meta:
        db_table = 'waiting_queue'


class ProcessedVideo(BaseModel):
    video = pw.ForeignKeyField(Video, backref="processed")
    manifest = pw.CharField()

    class Meta:
        db_table = 'processed_video'
