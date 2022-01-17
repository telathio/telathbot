import httpx
import typer


def main(
    url: str = typer.Option(
        ..., help="Fully formed URL (i.e. http://telathbot.com", envvar="TELATHBOT_URL"
    )
):
    typer.echo("Starting TelathBot SafetyTools checks.")
    ip_check_resp = httpx.post(
        f"{url}/metadata/check/ip",
        headers={"content-type": "application/json"},
        json={"ip": ""},
    )
    if ip_check_resp.status_code != 200:
        raise Exception("Error checking public IP.")

    typer.echo("TelathBot public IP unchanged, scraping SafetyTools uses.")
    safetytools_params = {"notify": True, "persist": True}
    safetools_response = httpx.get(
        f"{url}/safetytools/uses/red", params=safetytools_params
    )
    if safetools_response.status_code != 200:
        raise Exception("Error reporting on safetytools.")
    typer.echo("Everything complete, exiting!.")


if __name__ == "__main__":
    typer.run(main)
