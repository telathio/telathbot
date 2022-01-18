import httpx
import typer


def main(
    url: str = typer.Option(
        ..., help="Fully formed URL (i.e. http://telathbot.com", envvar="TELATHBOT_URL"
    )
):
    typer.echo("Starting TelathBot SafetyTools checks.")
    ip_check_resp = httpx.post(
        f"{url}/appdata/check/ip",
        headers={"content-type": "application/json"},
        json={"ip": ""},
    )
    if ip_check_resp.status_code != 200:
        raise Exception("Error checking public IP.")

    typer.echo("TelathBot public IP unchanged, scraping SafetyTools uses.")
    safetools_scrape_response = httpx.post(
        f"{url}/safetytools/uses/red"
    )
    if safetools_scrape_response.status_code != 200:
        raise Exception("Error scraping on safetytools.")

    typer.echo("TelathBot scraping complete, notifying of uses.")
    safetools_scrape_response = httpx.post(
        f"{url}/safetytools/notify/red"
    )
    if safetools_scrape_response.status_code != 200:
        raise Exception("Error notifying on safetytools.")
    
    typer.echo("Everything complete, exiting!.")


if __name__ == "__main__":
    typer.run(main)
