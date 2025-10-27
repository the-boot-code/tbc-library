# kokoro_tts.py

import base64
import io
import warnings
import asyncio
import numpy as np
import soundfile as sf
from python.helpers import runtime
from python.helpers.print_style import PrintStyle
from python.helpers.notification import NotificationManager, NotificationType, NotificationPriority

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

_pipeline = None
_voice = "am_puck,am_onyx"
_speed = 1.1
is_updating_model = False


async def preload():
    try:
        # return await runtime.call_development_function(_preload)
        return await _preload()
    except Exception as e:
        # if not runtime.is_development():
        raise e
        # Fallback to direct execution if RFC fails in development
        # PrintStyle.standard("RFC failed, falling back to direct execution...")
        # return await _preload()


async def _preload():
    global _pipeline, is_updating_model

    while is_updating_model:
        await asyncio.sleep(0.1)

    try:
        is_updating_model = True
        if not _pipeline:
            NotificationManager.send_notification(
                NotificationType.INFO,
                NotificationPriority.NORMAL,
                "Loading Kokoro TTS model...",
                display_time=99,
                group="kokoro-preload")
            PrintStyle.standard("Loading Kokoro TTS model...")
            from kokoro import KPipeline
            _pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
            NotificationManager.send_notification(
                NotificationType.INFO,
                NotificationPriority.NORMAL,
                "Kokoro TTS model loaded.",
                display_time=2,
                group="kokoro-preload")
    finally:
        is_updating_model = False


async def is_downloading():
    try:
        # return await runtime.call_development_function(_is_downloading)
        return _is_downloading()
    except Exception as e:
        # if not runtime.is_development():
        raise e
        # Fallback to direct execution if RFC fails in development
        # return _is_downloading()


def _is_downloading():
    return is_updating_model

async def is_downloaded():
    try:
        # return await runtime.call_development_function(_is_downloaded)
        return _is_downloaded()
    except Exception as e:
        # if not runtime.is_development():
        raise e
        # Fallback to direct execution if RFC fails in development
        # return _is_downloaded()

def _is_downloaded():
    return _pipeline is not None


async def synthesize_sentences(sentences: list[str]):
    """Generate audio for multiple sentences and return concatenated base64 audio"""
    try:
        # return await runtime.call_development_function(_synthesize_sentences, sentences)
        return await _synthesize_sentences(sentences)
    except Exception as e:
        # if not runtime.is_development():
        raise e
        # Fallback to direct execution if RFC fails in development
        # return await _synthesize_sentences(sentences)


async def _synthesize_sentences(sentences: list[str]) -> str:
    await _preload()
    
    try:
        audio_chunks = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            segments = _pipeline(sentence.strip(), voice=_voice, speed=_speed)  # type: ignore
            
            for segment in segments:
                audio_numpy = segment.audio.detach().cpu().numpy()  # type: ignore
                audio_chunks.append(audio_numpy)
                del segment  # Explicitly free PyTorch tensor memory
        
        # Concatenate all audio chunks at once
        if not audio_chunks:
            PrintStyle.warning("No audio generated - all sentences were empty")
        
        combined_audio = np.concatenate(audio_chunks) if audio_chunks else np.array([])
        
        # Write as single WAV file
        buffer = io.BytesIO()
        sf.write(buffer, combined_audio, 24000, format="WAV")
        audio_bytes = buffer.getvalue()
        
        # Return base64 encoded audio
        return base64.b64encode(audio_bytes).decode("utf-8")

    except Exception as e:
        PrintStyle.error(f"Error in Kokoro TTS synthesis: {e}")
        raise


async def synthesize_sentences_streaming(sentences: list[str]):
    """Generate audio for sentences and yield base64 audio chunks as they're ready"""
    try:
        async for chunk in _synthesize_sentences_streaming(sentences):
            yield chunk
    except Exception as e:
        raise e


async def _synthesize_sentences_streaming(sentences: list[str]):
    """Stream audio chunks sentence-by-sentence to reduce latency"""
    await _preload()
    
    try:
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            segments = _pipeline(sentence.strip(), voice=_voice, speed=_speed)  # type: ignore
            sentence_audio = []
            
            for segment in segments:
                audio_numpy = segment.audio.detach().cpu().numpy()  # type: ignore
                sentence_audio.append(audio_numpy)
                del segment  # Explicitly free PyTorch tensor memory
            
            if not sentence_audio:
                continue
            
            # Concatenate this sentence's audio
            combined_audio = np.concatenate(sentence_audio)
            
            # Write as WAV file
            buffer = io.BytesIO()
            sf.write(buffer, combined_audio, 24000, format="WAV")
            audio_bytes = buffer.getvalue()
            
            # Yield this sentence's audio immediately
            yield base64.b64encode(audio_bytes).decode("utf-8")
            
    except Exception as e:
        PrintStyle.error(f"Error in Kokoro TTS streaming synthesis: {e}")
        raise