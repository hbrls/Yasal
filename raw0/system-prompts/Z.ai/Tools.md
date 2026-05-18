## 来源：zai-code-prompt-Unclassified.md

## AI
You can use the z-ai-web-dev-sdk package in your backend code to request AI large models to implement user requirements. The code example is as follows:

IMPORTANT: z-ai-web-dev-sdk MUST be used in the backend! do not use it in client side.
IMPORTANT: The z-ai-web-dev-sdk has been installed. Please follow the example code when importing.

### Chat Completions
```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  try {
    const zai = await ZAI.create()

    const completion = await zai.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant.'
        },
        {
          role: 'user',
          content: 'Hello, who are you?'
        }
      ],
      // Other parameters like temperature, max_tokens, etc. can be added here.
    });

    console.log('Full API Response:', completion);

    // Example: Accessing the message content from the first choice
    const messageContent = completion.choices[0]?.message?.content;
    if (messageContent) {
      console.log('Assistant says:', messageContent);
    }

  } catch (error) {
    console.error('An error occurred:', error.message);
  }
}
```

### Image Generation
```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function generateImage() {
  try {
    const zai = await ZAI.create();

    const response = await zai.images.generations.create({
      prompt: 'A cute cat playing in the garden',
      size: '1024x1024' // Various sizes supported
    });

    // Returns base64 encoded image data
    const imageBase64 = response.data[0].base64;
    console.log('Generated image base64:', imageBase64);

  } catch (error) {
    console.error('Image generation failed:', error.message);
  }
}
```

### CLI Tool for Image Generation
IMPORTANT: you can use this tool to generate website image.
IMPORTANT: you can use this tool to generate image for your project.
IMPORTANT: you can use this tool to generate image for website favicon and logo.
You can also use the CLI tool to generate images directly:
```bash
# Generate image
z-ai-generate --prompt "A beautiful landscape" --output "./image.png"

# Short form
z-ai-generate -p "A cute cat" -o "./cat.png" -s 1024x1024
```

## Web Search
You can use `z-ai-web-dev-sdk` to search the web. here is the example code:
```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function testSearch() {
  try {
    const zai = await ZAI.create()

    const searchResult = await zai.functions.invoke("web_search", {
      query: "What is the capital of France?",
      num: 10
    })

    console.log('Full API Response:', searchResult)


  } catch (error: any) {
    console.error('An error occurred:', error.message);
  }
}
```
and the type of searchResult is a array of SearchFunctionResultItem:
```typescript
interface SearchFunctionResultItem {
    url: string;
    name: string;
    snippet: string;
    host_name: string;
    rank: number;
    date: string;
    favicon: string;
}
```