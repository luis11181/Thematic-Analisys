import OpenAI from 'openai';
import fs from 'fs';
//require('dotenv').config();
//import dotenv as import
import dotenv from 'dotenv';
dotenv.config();

const openai = new OpenAI({
  apiKey: process.env["OPENAI_API_KEY"]
});

async function main() {
  const content = fs.readFileSync('Question.txt', 'utf-8');

  const params = {
    messages: [{ role: 'user', content }],
    model: 'gpt-4-0613',
    n: 1,
    temperature: 0,
    max_tokens: 1000,
  };

  const completion = await openai.chat.completions.create(params);

  const response = completion.choices[0]?.message?.content;
  fs.writeFileSync('response.txt', response);

 console.log(response);
}


main();