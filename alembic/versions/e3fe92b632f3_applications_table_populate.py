"""applications table Populate

Revision ID: e3fe92b632f3
Revises: 0bdc7eb11c7f
Create Date: 2025-04-05 23:40:44.122023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e3fe92b632f3'
down_revision: Union[str, None] = '0bdc7eb11c7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'applications',
        sa.Column('application_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('visa_request_id', sa.Integer, sa.ForeignKey('visa_request.visa_request_id'), nullable=False),
        sa.Column('application_code', sa.String(50), nullable=False, unique=True),
        sa.Column('applicant_first_name', sa.String(100), nullable=False),
        sa.Column('applicant_middle_name', sa.String(100), nullable=True),
        sa.Column('applicant_last_name', sa.String(100), nullable=True),
        sa.Column('applicant_email', sa.String(100), nullable=False),
        sa.Column('applicant_phone', sa.String(20), nullable=False),
        sa.Column('applicant_passport_number', sa.String(50), nullable=False),
        sa.Column('applicant_dob', sa.DateTime, nullable=False),
        sa.Column('applicant_gender', sa.Enum('MALE', 'FEMALE', 'OTHER', name='gender_enum'), nullable=False),
        sa.Column('visa_status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'PROCESSING', name='application_visa_status_enum'), default='PENDING'),
        sa.Column('submission_date', sa.DateTime, server_default=sa.func.now()),
        sa.Column('modified_date', sa.DateTime, onupdate=sa.func.now()),
        sa.Column('active_status', sa.Boolean, default=True),
        sa.Column('assigned_to', sa.Integer, nullable=True),
        sa.Column('assigned_to_name', sa.String(100), nullable=True),
        sa.Column('expected_completion_date', sa.DateTime, nullable=True),
        sa.Column('application_notes', sa.String, nullable=True),
        sa.Column('is_priority', sa.Boolean, default=False),
        sa.Column('is_escilated', sa.Boolean, default=False)
    )

    op.create_table(
        'application_details',
        sa.Column('application_detail_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('application_id', sa.Integer, sa.ForeignKey('applications.application_id'), nullable=False),
        sa.Column('document_code', sa.String(50), nullable=False, unique=True),
        sa.Column('field_name', sa.String(100), nullable=False),
        sa.Column('field_value', sa.String(100), nullable=False),
        sa.Column('field_title', sa.String(100), nullable=False),
        sa.Column('field_description', sa.String(255), nullable=True),
        sa.Column('field_type', sa.Enum('TEXT', 'NUMBER', 'DATE', 'DOCUMENT', name='field_type_enum'), nullable=False),
        sa.Column('document_type', sa.Enum('PASSPORT', 'PHOTO', 'VISA_FORM', 'OTHER', name='document_type_enum'), nullable=False),
        sa.Column('uploaded_date', sa.DateTime, server_default=sa.func.now()),
        sa.Column('verification_status', sa.Enum('PENDING', 'VERIFIED', 'REJECTED', name='verification_status_enum'), default='PENDING'),
        sa.Column('remark', sa.String, nullable=True),
        sa.Column('verified_by', sa.Integer, nullable=True),
        sa.Column('verified_date', sa.DateTime, nullable=True),
        sa.Column('active_status', sa.Boolean, default=True)
    )

    op.create_table(
        'application_remarks',
        sa.Column('remark_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('application_id', sa.Integer, sa.ForeignKey('applications.application_id'), nullable=False),
        sa.Column('remark_type', sa.Enum('GENERAL', 'VERIFICATION', 'ESCALATION', name='remark_type_enum'), nullable=False),
        sa.Column('remark_text', sa.String, nullable=False),
        sa.Column('created_by', sa.Integer, nullable=False),
        sa.Column('created_date', sa.DateTime, server_default=sa.func.now()),
        sa.Column('modified_by', sa.Integer, nullable=True),
        sa.Column('modified_date', sa.DateTime, onupdate=sa.func.now()),
        sa.Column('is_internal', sa.Enum('YES', 'NO', name='is_internal_enum'), default='NO')
    )

    op.create_table(
        'application_assignment_history',
        sa.Column('assignment_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('application_id', sa.Integer, sa.ForeignKey('applications.application_id'), nullable=False),
        sa.Column('assigned_by', sa.Integer, nullable=False),
        sa.Column('assigned_to', sa.Integer, nullable=False),
        sa.Column('assigned_date', sa.DateTime, server_default=sa.func.now()),
        sa.Column('assignment_status', sa.Enum('ASSIGNED', 'REASSIGNED', 'UNASSIGNED', name='assignment_status_enum'), nullable=False),
        sa.Column('remarks', sa.String, nullable=True)
    )


def downgrade() -> None:
    # Drop Tables
    op.drop_table('application_assignment_history')
    op.drop_table('application_remarks')
    op.drop_table('application_details')
    op.drop_table('applications')

    # Drop Enums
    op.execute('DROP TYPE IF EXISTS gender_enum')
    op.execute('DROP TYPE IF EXISTS application_visa_status_enum')
    op.execute('DROP TYPE IF EXISTS field_type_enum')
    op.execute('DROP TYPE IF EXISTS document_type_enum')
    op.execute('DROP TYPE IF EXISTS verification_status_enum')
    op.execute('DROP TYPE IF EXISTS remark_type_enum')
    op.execute('DROP TYPE IF EXISTS is_internal_enum')
    op.execute('DROP TYPE IF EXISTS assignment_status_enum')

