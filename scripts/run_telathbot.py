import httpx
import typer


def main(
    url: str = typer.Option(
        ..., help="Fully formed URL (i.e. http://telathbot.com", envvar="TELATHBOT_URL"
    )
):
    ip_check_resp = httpx.post(f"{url}/metadata/check/ip", data={})
    if ip_check_resp.status_code != 200:
        raise Exception("Error checking public IP.")

    safetytools_params = {"notify": True, "persist": True}
    safetools_response = httpx.get(
        f"{url}/safetytools/level/red", params=safetytools_params
    )
    if safetools_response.status_code != 200:
        raise Exception("Error reporting on safetytools.")


if __name__ == "__main__":
    typer.run(main)
