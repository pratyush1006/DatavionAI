"""Forward-only live tracking migration; existing 0001 is untouched."""

from __future__ import annotations
import uuid
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [("geography", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="TrackingSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("tenant_id", models.UUIDField(db_index=True)),
                (
                    "organization_id",
                    models.UUIDField(blank=True, db_index=True, null=True),
                ),
                ("subject_type", models.CharField(max_length=64)),
                ("subject_id", models.CharField(max_length=128)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="active",
                        max_length=16,
                    ),
                ),
                ("created_by_id", models.UUIDField(db_index=True)),
                ("started_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("ended_at", models.DateTimeField(blank=True, null=True)),
                ("last_seen_at", models.DateTimeField(blank=True, null=True)),
                (
                    "last_latitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "last_longitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "last_accuracy_meters",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("metadata", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "db_table": "geography_tracking_sessions",
                "ordering": ("-started_at",),
            },
        ),
        migrations.CreateModel(
            name="TrackingParticipant",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("user_id", models.UUIDField(db_index=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("owner", "Owner"),
                            ("updater", "Updater"),
                            ("viewer", "Viewer"),
                        ],
                        max_length=16,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participants",
                        to="geography.trackingsession",
                    ),
                ),
            ],
            options={"db_table": "geography_tracking_participants"},
        ),
        migrations.CreateModel(
            name="LocationUpdate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("sequence", models.PositiveBigIntegerField()),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                (
                    "accuracy_meters",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "altitude_meters",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "speed_mps",
                    models.DecimalField(
                        blank=True, decimal_places=3, max_digits=10, null=True
                    ),
                ),
                (
                    "heading_degrees",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                ("recorded_at", models.DateTimeField()),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("source", models.CharField(default="device", max_length=32)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to="geography.trackingsession",
                    ),
                ),
            ],
            options={
                "db_table": "geography_location_updates",
                "ordering": ("-recorded_at", "-sequence"),
            },
        ),
        migrations.AddConstraint(
            model_name="trackingparticipant",
            constraint=models.UniqueConstraint(
                fields=("session", "user_id"), name="geo_track_participant_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="locationupdate",
            constraint=models.UniqueConstraint(
                fields=("session", "sequence"),
                name="geo_track_location_sequence_unique",
            ),
        ),
        migrations.AddIndex(
            model_name="trackingsession",
            index=models.Index(
                fields=("tenant_id", "status"), name="geo_track_tenant_status"
            ),
        ),
        migrations.AddIndex(
            model_name="trackingsession",
            index=models.Index(
                fields=("subject_type", "subject_id"), name="geo_track_subject"
            ),
        ),
        migrations.AddIndex(
            model_name="trackingsession",
            index=models.Index(
                fields=("organization_id", "status"), name="geo_track_org_status"
            ),
        ),
        migrations.AddIndex(
            model_name="trackingparticipant",
            index=models.Index(
                fields=("user_id", "is_active"), name="geo_track_part_user"
            ),
        ),
        migrations.AddIndex(
            model_name="locationupdate",
            index=models.Index(
                fields=("session", "recorded_at"), name="geo_track_loc_time"
            ),
        ),
    ]
