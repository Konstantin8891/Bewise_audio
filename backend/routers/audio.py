import os

import aiofiles

from typing import BinaryIO

from fastapi import APIRouter, status, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydub import AudioSegment
from sqlalchemy.orm import Session
from uuid import UUID

from .users import get_db

import sys
sys.path.append('..')

from models import Audio, User
from settings import RECORDS_DIR


router = APIRouter(prefix='', tags=['audio_router'])


@router.post('/create_audio', status_code=status.HTTP_201_CREATED)
async def create_audio(
    user_id: int, uuid: UUID, audio: UploadFile, db: Session = Depends(get_db)
) -> str:
    user_instance = db.query(User).filter(
        User.id == user_id
    ).filter(User.uuid == uuid).first()
    if not user_instance:
        raise HTTPException(status_code=400, detail='User or token not found')

    filename_wav = '1.wav'
    file_location_wav = RECORDS_DIR + '/' + filename_wav

    async with aiofiles.open(file_location_wav, 'wb') as record:
        content = await audio.read()
        await record.write(content)

    filename_mp3 = '1.mp3'
    name_counter = 1
    while True:
        if filename_mp3 in os.listdir(RECORDS_DIR):
            name_counter += 1
            filename_mp3 = f'{name_counter}.mp3'
        else:
            break

    file_location_mp3 = RECORDS_DIR + '/' + filename_mp3
    AudioSegment.from_wav(file_location_wav).export(
        file_location_mp3, format="mp3"
    )
    os.remove(file_location_wav)

    audio_instance = Audio(
        name=filename_mp3,
        user_id=user_id
    )
    db.add(audio_instance)
    db.commit()
    db.refresh(audio_instance)
    return f'http://localhost:8000/record?id={audio_instance.id}&user={user_id}'


@router.get('/record', response_model=None)
async def get_audio(
    id: UUID, user: int, db: Session = Depends(get_db)
) -> BinaryIO:
    user_instance = db.query(User).filter(User.id == user).first()
    if not user_instance:
        raise HTTPException(status_code=400, detail='User not found')
    audio_instance = db.query(Audio).filter(Audio.id == id).first()
    if not audio_instance:
        raise HTTPException(status_code=400, detail='Audio file not found')
    file_location_mp3 = RECORDS_DIR + '/' + audio_instance.name
    return FileResponse(
        path=file_location_mp3,
        media_type='application/octet-stream'
    )
