import React, { useState } from 'react';
import { View, TextInput, Button, Text, ScrollView } from 'react-native';

export default function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<string[]>([]);

  const send = async () => {
    const body = { messages: [{ role: 'user', content: input }] };
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    setMessages([...messages, input, data.content || JSON.stringify(data)]);
    setInput('');
  };

  return (
    <View style={{ padding: 20 }}>
      <ScrollView>{messages.map((m, i) => <Text key={i}>{m}</Text>)}</ScrollView>
      <TextInput value={input} onChangeText={setInput} style={{ borderWidth: 1 }} />
      <Button title="Send" onPress={send} />
    </View>
  );
}
