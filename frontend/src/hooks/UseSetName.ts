import { useState } from 'react';

export function useSetName() {
  const [name, setName] = useState("");

  const generateRandom = () => {
    const Adjectives: string[] = [
      "Angry",
      "Flying",
      "Hostile",
      "Green",
      "Old",
      "Broken",
      "[Error]",
    ];
    const Nouns: string[] = ["jumper", "Benjamin", "dog", "[Error]", "bird"];
    
    const adjective = Adjectives[Math.floor(Math.random() * Adjectives.length)]
    const noun = Nouns[Math.floor(Math.random() * Nouns.length)]

    setName(`${adjective} ${noun}`);
  };

  function read (input: string) {
    setName(input);
  };

  return [name, generateRandom, read] as const;
}
