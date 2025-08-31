import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import Chat from './screens/Chat';

export default function App() {
  return (
    <NavigationContainer>
      <Chat />
    </NavigationContainer>
  );
}
