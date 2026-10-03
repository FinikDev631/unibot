import json
import mimetypes
import urllib.error
import urllib.parse
import urllib.request

from ..exceptions import BotAPIError, NetworkError
from ..types import normalize_file


class BaseAdapter:
    def __init__(self, token, base_url, path_template="/bot{token}/{method}", timeout=30):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.path_template = path_template
        self.timeout = timeout

    def _url(self, method):
        return self.base_url + self.path_template.format(token=self.token, method=method)

    def request(self, method, data=None, files=None):
        data = dict(data or {})
        files = dict(files or {})

        try:
            if files:
                body, content_type = self._multipart(data, files)
            else:
                body = urllib.parse.urlencode(self._clean_data(data)).encode()
                content_type = "application/x-www-form-urlencoded"

            request = urllib.request.Request(
                self._url(method),
                data=body,
                headers={"Content-Type": content_type, "User-Agent": "UniBot/0.1.0"},
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                status = response.status
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            status = exc.code
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise NetworkError(str(exc)) from exc

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            if status >= 400:
                raise NetworkError(f"HTTP {status}: {raw}") from None
            return raw

        if not payload.get("ok", False):
            raise BotAPIError(
                method=method,
                description=payload.get("description", ""),
                error_code=payload.get("error_code", status),
                parameters=payload.get("parameters"),
                response=payload,
            )

        return payload.get("result")

    def _clean_data(self, data):
        result = {}
        for key, value in data.items():
            if value is None:
                continue
            if isinstance(value, (dict, list, tuple)):
                result[key] = json.dumps(value, ensure_ascii=False)
            elif isinstance(value, bool):
                result[key] = "true" if value else "false"
            else:
                result[key] = str(value)
        return result

    def _multipart(self, data, files):
        boundary = "----UniBotBoundary7MA4YWxkTrZu0gW"
        chunks = []

        for key, value in self._clean_data(data).items():
            chunks.extend([
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            ])

        for field, value in files.items():
            filename, content = normalize_file(value)
            content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            chunks.extend([
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'.encode(),
                f"Content-Type: {content_type}\r\n\r\n".encode(),
                content,
                b"\r\n",
            ])

        chunks.append(f"--{boundary}--\r\n".encode())
        return b"".join(chunks), f"multipart/form-data; boundary={boundary}"
