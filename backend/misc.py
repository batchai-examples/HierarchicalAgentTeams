from __future__ import annotations

import base64
import mimetypes
from datetime import datetime
from typing import Any, Optional

from charset_normalizer import from_bytes
from fastapi import Request, UploadFile
from fsspec.asyn import AsyncFileSystem  # type: ignore

from const import Constants
from errs import BadRequest


def parse_datetime(v: Any) -> datetime | None:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, float):
        return datetime.fromtimestamp(v)
    if isinstance(v, int):
        return datetime.fromtimestamp(float(v))
    if isinstance(v, str):
        return datetime.strptime(v, Constants.DATETIME_FORMAT)
    raise BadRequest(f"Invalid datetime value: {v}")


def format_datetime(v: datetime) -> str:
    return None if v is None else v.strftime(Constants.DATETIME_FORMAT)


def guess_mime_type(p: str) -> str:
    r, _ = mimetypes.guess_type(p)
    return r or "application/octet-stream"


def detect_encoding(file_bytes: bytes) -> str:
    """
    Detect the encoding of a given byte sequence using charset-normalizer.

    :param file_bytes: The content of the file in bytes.
    :return: Detected encoding as a string.
    """
    result = from_bytes(file_bytes).best()
    return result.encoding if result is not None else ""


async def read_file_text(fs: AsyncFileSystem, p: str, encoding: Optional[str] = "utf-8") -> tuple[str, str]:
    f_bytes = await read_file_bytes(fs, p)
    if encoding is None:
        encoding = detect_encoding(f_bytes)
    return f_bytes.decode(encoding), encoding


async def write_file_text(fs: AsyncFileSystem, p: str, text: str, encoding: str = "utf-8"):
    t_bytes = text.encode(encoding)
    await write_file_bytes(fs, p, t_bytes)


async def read_file_bytes(fs: AsyncFileSystem, p: str) -> bytes:
    async with fs.open(p, mode="rb") as f:
        return await f.read()


async def write_file_bytes(fs: AsyncFileSystem, p: str, f_bytes: bytes):
    async with fs.open(p, mode="wb") as f:
        await f.write(f_bytes)


async def transfer_file(
    src_fs: AsyncFileSystem,
    src_p: str,
    dst_fs: AsyncFileSystem,
    dst_p: str,
    buf_size: int = 65536,
) -> tuple[int, bytes | None]:
    if buf_size is None or buf_size <= 2048:
        buf_size = 2048

    got = 0
    head: bytes | None = None

    async with src_fs.open(src_p, mode="rb") as src_f:
        async with dst_fs.open(dst_p, "wb") as dst_f:
            while True:
                chunk: bytes = await src_f.read(buf_size)
                if not chunk:
                    break

                if head is None:
                    head = chunk

                await dst_f.write(chunk)
                got += len(chunk)

    return got, head


async def transfer_stream(
    src: UploadFile, dst_fs: AsyncFileSystem, dst_p: str, buf_size: int = 65536
) -> tuple[int, bytes]:
    if buf_size is None or buf_size <= 2048:
        buf_size = 2048

    got = 0
    head: bytes = b""

    async with dst_fs.open(dst_p, "wb") as dst_f:
        while True:
            chunk = await src.read(buf_size)  # Use the async read method
            if not chunk:
                break
            if not head:
                head = chunk

            await dst_f.write(chunk)
            got += len(chunk)

    return got, head


def parse_data_url(data_url: str) -> tuple[str, str, bytes]:
    """
    Parse the Data URL and return the MIME type, encoding, and data.
    :param data_url: The Data URL to parse.
    :return: A tuple containing the MIME type, encoding, and decoded data as bytes.
    """
    if not data_url.startswith("data:"):
        raise ValueError(f"Invalid data URL: {data_url}")

    header, encoded_data = data_url.split(",", 1)
    mime_type, encoding = header.split(";")[0][5:], header.split(";")[1]
    if encoding != "base64":
        raise ValueError("Only base64 encoding is supported")

    data = base64.b64decode(encoded_data)
    return mime_type, encoding, data


def get_str_header(req: Request, name: str, devault: str) -> str:
    return req.headers.get(name) or devault


def get_int_header(req: Request, name: str, devault: int) -> int:
    s = req.headers.get(name)
    return int(s) if s else devault


def get_bool_header(req: Request, name: str, devault: bool) -> bool:
    s = req.headers.get(name)
    return s == "true" if s else devault


def get_client_ip(req: Request) -> str:
    h = req.headers

    x_forwarded_for = h.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    real_ip = req.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    if req.client:
        return req.client.host
    return ""


def get_client_port(req: Request) -> int:
    x_forwarded_port = req.headers.get("f-forwarded-port")
    if x_forwarded_port:
        return int(x_forwarded_port)
    if req.client:
        return req.client.port
    return 0


def get_client_proto(req: Request) -> str:
    x_forwarded_proto = req.headers.get("x-forwarded-proto")
    if x_forwarded_proto:
        return x_forwarded_proto
    if req.client:
        return req.url.scheme
    return ""


def get_client_proxy_chain(req: Request) -> list[str]:
    x_forwarded_for = req.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return [ip.strip() for ip in x_forwarded_for.split(",")]
    return []


def basename(p: str) -> str:
    p = normalize_path(p)
    _, r = p.split("/", 1)
    return r


def normalize_path(p: str) -> str:
    if not p:
        return p
    p = p.lstrip("/").rstrip("/")

    components: list[str] = []
    for c in p.split("/"):
        if c in {"", "."}:
            break
        if c == "..":
            c = c[:-1]
        components.append(c)

    return "/".join(components)
