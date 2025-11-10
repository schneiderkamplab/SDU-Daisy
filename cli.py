import typer
from evaluation.eval import evaluate_dataset, run_eval
app = typer.Typer()

@app.command()
def eval(
    input: str = typer.Argument(..., help="Input string to be evaluated")
):
    typer.echo("Starting evaluation...")
    result = evaluate_dataset(input, gold_path="private/v_0.2_6_SDU-Culture-1.csv")
    typer.echo(f"Evaluation result: {result}")


@app.command()
def run(
    input_file: str = typer.Argument("public/questions.csv", help="Path to input CSV or Parquet file"),
    output_file: str = typer.Argument("predictions.csv", help="Path to output CSV file for predictions"),
    model: str = typer.Option(..., help="Model name to use for predictions"),
    base_url: str = typer.Option("http://localhost:8000/v1", help="Base URL for the OpenAI API"),
    api_key: str = typer.Option("", help="API key for the OpenAI API"),
    max_tokens: int = typer.Option(2000, help="Maximum tokens for the model response"),
    temperature: float = typer.Option(0.7, help="Temperature for the model response"),
):
    typer.echo("Running model evaluation...")
    run_eval(
        input_file=input_file,
        output_file=output_file,
        model=model,
        base_url=base_url,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
    )


if __name__ == "__main__":
    app()