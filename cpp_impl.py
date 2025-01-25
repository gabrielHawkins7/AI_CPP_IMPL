import os
import sys
import openai

def main():
    # Ensure the user provided a file as an argument
    if len(sys.argv) != 2:
        print("Usage: python cpp_impl.py <header_file.h>")
        sys.exit(1)

    header_file = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(header_file):
        print(f"File not found: {header_file}")
        sys.exit(1)

    # Read the contents of the header file
    with open(header_file, 'r') as file:
        header_content = file.read()

    # Prepare the prompt for the AI model
    prompt = f"""Generate the C++ implementation (.cpp) file for the following header file content Only respond with code as plain text without code block syntax around it:

{header_content}

Please provide the full implementation code with necessary includes and using statements."""

    # Set your API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    # Optionally set the API base URL, API type, and API version for OpenAI-compatible APIs
    # For example, when using the Azure OpenAI Service
    
    base_url = os.getenv("OPENAI_API_BASE_URL")
    if not base_url:
        print("Error: The OPENAI_API_BASE_URL environment variable is not set.")
        sys.exit(1)

    model_name = os.getenv("OPENAI_MODEL_NAME");
    if not model_name:
        print("Error: The OPENAI_MODEL_NAME environment variable is not set.")
        sys.exit(1)
    
    

    try:

        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )


        generated_code = response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred while communicating with the API: {e}")
        sys.exit(1)

    # Determine the output file name
    base_name = os.path.splitext(header_file)[0]
    cpp_file = f"{base_name}.cpp"

    # Save the generated code to the .cpp file
    with open(cpp_file, 'w') as file:
        file.write(generated_code)

    print(f"Generated implementation saved to {cpp_file}")

if __name__ == "__main__":
    main()
