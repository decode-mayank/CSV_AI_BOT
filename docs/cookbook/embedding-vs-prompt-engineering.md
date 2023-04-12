### Embedding vs Prompt Engineering

### Embedding 

Embedding is the method where we can have a file and train them. Embedding will calculate cosine similarity between the resulting query embedding and each of the function embeddings. The highest cosine similarity results are most relevant. There is a certain format to train the data that openai provides https://platform.openai.com/docs/guides/embeddings/what-are-embeddings 

## Reference

    1. https://bitcot.atlassian.net/wiki/spaces/BitcotAI1/pages/181469185/Train+the+model

    2. https://bitcot.atlassian.net/wiki/spaces/BitcotAI1/pages/182452274/Best+approach+to+design+chatbot+-+Embedding

### Prompt

Prompt is one of the openai parameters where the context that has to be given inside the prompt then for each query it will check the prompt and answer accordingly.

### Embedding vs Prompt Engineering

We have choosed prompt engineering as it can answer to any type of questions but in embeddings since it will have text similarities it can provide irrelevant answers.

Reference - https://bitcot.atlassian.net/wiki/spaces/BitcotAI1/pages/202768470/Embeddings+vs+Prompt+-+Is+it+necessary+to+ask+the+consumer+for+more+details+about+their+symptoms

## usecase
### Prompt Engineering

Use case: Customer service chatbot

Objective: Develop a chatbot that can provide customer support to users with product-related queries.

Techniques used:

Prompt engineering: Prompts are carefully crafted to guide the chatbot towards generating responses that address user queries and provide helpful information. This involves using prompts that include relevant product features, troubleshooting tips, and frequently asked questions.

Example interaction:
User: How do I reset my password?
Chatbot: I'm sorry to hear that you're having trouble with your password. Let's see if we can get that sorted out for you. Have you tried using the password reset link in your account settings? If that doesn't work, you can also contact our support team at [email protected] and they will be happy to assist you further.

In this use case, prompt engineering is used to guide the chatbot towards generating a helpful response to a user's product-related query. The prompt includes troubleshooting tips and a contact email address for further assistance, which helps to address the user's concerns and provide them with relevant information. By using prompt engineering to guide the chatbot's responses, the chatbot is able to provide a helpful and efficient customer service experience for users.

### Embedding

Use case: News recommendation chatbot

Objective: Develop a chatbot that can recommend news articles to users based on their interests.

Techniques used:

Embeddings: Word embeddings are used to represent news articles and user interests, allowing the chatbot to identify patterns and recommend relevant articles.

Example interaction:
User: I'm interested in technology news.
Chatbot: Great! Here are some recent articles you might be interested in:

"Apple Unveils New MacBook Pro with M1 Pro and M1 Max Chips"
"Facebook Faces Criticism Over New 'Instagram for Kids' App"
"Tesla Reports Record Q3 Profits Thanks to Strong Sales and Cost-Cutting Measures"

In this use case, embeddings are used to represent news articles and user interests, allowing the chatbot to identify patterns and recommend relevant articles. By representing articles and user interests using embeddings, the chatbot is able to identify similarities and recommend articles that are likely to be of interest to the user. This allows the chatbot to provide a personalized news recommendation service to users, improving the user experience and engagement with the chatbot.

