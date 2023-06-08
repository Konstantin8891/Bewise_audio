import os

import aiofiles

from typing import BinaryIO

from fastapi import APIRouter, status, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydub import AudioSegment
from sqlalchemy import select
from sqlalchemy.ext import asyncio as sea
from uuid import UUID

from database import get_async_session
from models import Audio, User
from settings import RECORDS_DIR


router = APIRouter(prefix='', tags=['audio_router'])


@router.post('/create_audio', status_code=status.HTTP_201_CREATED)
async def create_audio(
    user_id: int,
    uuid: UUID,
    audio: UploadFile,
    db: sea.AsyncSession = Depends(get_async_session)
) -> str:
    user_instance = await db.execute(select(User).where(
        User.uuid == uuid
    ))
    user_instance = user_instance.scalar_one_or_none()
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
    try:
        AudioSegment.from_wav(file_location_wav).export(
            file_location_mp3, format="mp3"
        )
    except Exception:
        raise HTTPException(
            status_code=400, detail='Something wrong with your audio file'
        )
    os.remove(file_location_wav)

    audio_instance = Audio(
        name=filename_mp3,
        user_id=user_id
    )
    db.add(audio_instance)
    await db.commit()
    await db.refresh(audio_instance)
    return (
        f'http://localhost:8000/record?id={audio_instance.id}&user={user_id}'
    )


@router.get('/record', response_model=None)
async def get_audio(
    id: UUID, user: int, db: sea.AsyncSession = Depends(get_async_session)
) -> BinaryIO:
    user_instance = await db.execute(select(User).where(User.id == user))
    user_instance = user_instance.scalar_one_or_none()
    if not user_instance:
        raise HTTPException(status_code=400, detail='User not found')
    audio_instance = await db.execute(select(Audio).where(Audio.id == id))
    audio_instance = audio_instance.scalar_one_or_none()
    if not audio_instance:
        raise HTTPException(status_code=400, detail='Audio file not found')
    file_location_mp3 = RECORDS_DIR + '/' + audio_instance.name
    return FileResponse(
        path=file_location_mp3,
        media_type='application/octet-stream'
    )
