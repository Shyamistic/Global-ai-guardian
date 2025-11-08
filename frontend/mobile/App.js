import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';

export default function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  async function askAPI() {
    let res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `question=${encodeURIComponent(question)}`
    });
    let data = await res.json();
    setAnswer(data.answer);
  }
  return (
    <View>
      <TextInput placeholder="Ask me..." value={question} onChangeText={setQuestion}/>
      <Button title="Ask" onPress={askAPI}/>
      <Text>{answer}</Text>
    </View>
  );
}
