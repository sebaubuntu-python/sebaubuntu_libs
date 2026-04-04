#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
from io import BytesIO
from pathlib import Path
from sebaubuntu_libs.libgofile import raw_api
from sebaubuntu_libs.libgofile.account import Account
from sebaubuntu_libs.libgofile.contents import ContentResponse, Folder
from typing import Iterable, Optional, Union


def get_server() -> str:
    """Returns the best server available to receive files."""
    return raw_api.get_server()["server"]


def upload_file(
    file: Union[str, Path, BytesIO],
    server: Optional[str] = None,
    token: Optional[str] = None,
    folder_id: Optional[str] = None,
    description: Optional[str] = None,
    password: Optional[str] = None,
    tags: Optional[Iterable[str]] = None,
    expire: Optional[datetime] = None,
):
    """Upload one file on a specific server."""
    if server is None:
        server = get_server()

    needs_open = not isinstance(file, BytesIO)

    if needs_open:
        with open(file, "rb") as f:
            data = raw_api.upload_file(
                server=server,
                file=f,  # type: ignore
                token=token,
                folder_id=folder_id,
                description=description,
                password=password,
                tags=",".join(tags) if tags else None,
                expire=expire,
            )
    else:
        data = raw_api.upload_file(
            server=server,
            file=file,
            token=token,
            folder_id=folder_id,
            description=description,
            password=password,
            tags=",".join(tags) if tags else None,
            expire=expire,
        )

    return data


def get_content(content_id: str, token: str):
    """Get a specific content details."""
    data = raw_api.get_content(content_id, token)

    return ContentResponse.from_dict(data)


def create_folder(parent_folder_id: str, folder_name: str, token: str):
    """Create a new folder."""
    data = raw_api.create_folder(parent_folder_id, folder_name, token)

    return Folder.from_dict(data)


def set_folder_option(token: str, folder_id: str, option: str, value: str):
    """Set an option on a folder."""
    raw_api.set_folder_option(token, folder_id, option, value)

    return True


def copy_content(contents_id: Iterable[str], folder_id_dest: str, token: str):
    """Copy one or multiple contents to another folder."""
    raw_api.copy_content(
        contents_id=",".join(contents_id),
        folder_id_dest=folder_id_dest,
        token=token,
    )

    return True


def delete_content(contents_id: Iterable[str], token: str):
    """Delete one or multiple files/folders."""
    raw_api.delete_content(
        contents_id=",".join(contents_id),
        token=token,
    )

    return True


def get_account(token: str):
    """Get the account details."""
    # As of now toggling all_details does nothing
    data = raw_api.get_account_details(token, True)

    return Account.from_dict(data)
