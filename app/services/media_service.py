import os
from datetime import datetime
import uuid
from fastapi import UploadFile, HTTPException
from typing import List

from app.api.application.application_types import BulkMediaUploadResponse, MediaUploadResponse
from app.config.aws import AWSService

aws_service = AWSService()

class MediaService:
    
    @staticmethod
    def generate_s3_path(visa_request_code: str, application_code: str, filename: str) -> str:
        """
        Generate consistent S3 path
        Format: visa_requests/{visa_request_code}/{application_code}/{uuid_filename}
        """
        # Generate unique filename
        ext = os.path.splitext(filename)[1]
        unique_id = str(uuid.uuid4())
        new_filename = f"{unique_id}{ext}"
        
        return f"visa_requests/{visa_request_code}/{application_code}/{new_filename}"

    async def upload_media(
        self,
        visa_request_code: str,
        application_code: str,
        files: List[UploadFile],
        max_size_mb: int = 10
    ) -> BulkMediaUploadResponse:
        """
        Upload multiple files for an application
        Args:
            visa_request_code: VR code from path
            application_code: Application code from path
            files: List of UploadFiles
            max_size_mb: Max file size in MB
        Returns:
            BulkMediaUploadResponse with S3 URLs
        """
        uploaded_files = []
        
        for file in files:
            # Validate file size
            if not aws_service.validate_file_size(file, max_size_mb):
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds maximum size of {max_size_mb}MB"
                )
            
            # Generate S3 path
            s3_key = self.generate_s3_path(visa_request_code, application_code, file.filename)
            
            try:
                # Upload file
                file_url = await aws_service.upload_upload_file(file, s3_key)
                preview_url = aws_service.generate_presigned_url(s3_key)
                
                uploaded_files.append(MediaUploadResponse(
                    file_url=file_url,
                    preview_url=preview_url,
                    s3_key=s3_key
                ))
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload {file.filename}: {str(e)}"
                )
        
        return BulkMediaUploadResponse(
            uploaded_files=uploaded_files,
            visa_request_code=visa_request_code,
            application_code=application_code
        )