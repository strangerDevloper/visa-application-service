"""Tables Populate

Revision ID: 0bdc7eb11c7f
Revises: af86ae65aee2
Create Date: 2025-04-05 22:44:01.397581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0bdc7eb11c7f'
down_revision: Union[str, None] = 'af86ae65aee2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Define the enum types
    payment_status_enum = sa.Enum('PENDING', 'PARTIAL', 'PAID', 'REFUNDED', name='payment_status_enum')  # Important for existing enums
    
    coupon_type_enum = sa.Enum('FLAT', 'PERCENTAGE', name='coupon_type_enum')
    
    visa_status_enum = sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'PROCESSING', name='visa_status_enum')

    # Create visa_request table
    op.create_table(
        'visa_request',
        sa.Column('visa_request_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('visa_request_code', sa.String(50), nullable=False, unique=True),
        sa.Column('visa_process_id', sa.Integer, nullable=False),
        sa.Column('visa_type', sa.String(50), nullable=False),
        sa.Column('country_id', sa.Integer, nullable=False),
        sa.Column('country_name', sa.String(100), nullable=False),
        sa.Column('initiator_name', sa.String(100), nullable=False),
        sa.Column('initiator_email', sa.String(100), nullable=False),
        sa.Column('initiator_phone', sa.String(20), nullable=False),
        sa.Column('initiator_address', sa.Text, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=True),
        sa.Column('vendor_id', sa.Integer, nullable=True),
        sa.Column('total_applicants', sa.Integer, nullable=False),
        sa.Column('application_fee', sa.Integer, nullable=False),
        sa.Column('visa_fee', sa.Integer, nullable=False),
        sa.Column('service_fee', sa.Integer, nullable=False),
        sa.Column('total_fee', sa.Integer, nullable=False),
        sa.Column('total_fee_currency', sa.String(10), nullable=False),
        sa.Column('amount_paid', sa.Integer, nullable=False),
        sa.Column('amount_due', sa.Integer, nullable=False),
        sa.Column('payment_status', payment_status_enum, default='PENDING'),
        sa.Column('payment_date', sa.DateTime, nullable=True),
        sa.Column('payment_reference', sa.String(100), nullable=True),
        sa.Column('coupon_code', sa.String(50), nullable=True),
        sa.Column('coupon_discount', sa.Integer, nullable=True),
        sa.Column('coupon_id', sa.Integer, nullable=True),
        sa.Column('coupon_type', coupon_type_enum, nullable=True),
        sa.Column('visa_status', visa_status_enum, default='PENDING'),
        sa.Column('created_date', sa.DateTime, server_default=sa.func.now()),
        sa.Column('modified_date', sa.DateTime, onupdate=sa.func.now()),
        sa.Column('active_status', sa.Boolean, default=True),
        sa.Column('visa_request_notes', sa.Text, nullable=True)
    )


def downgrade() -> None:
    # Drop the table first
    op.drop_table('visa_request')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS payment_status_enum")
    op.execute("DROP TYPE IF EXISTS coupon_type_enum")
    op.execute("DROP TYPE IF EXISTS visa_status_enum")