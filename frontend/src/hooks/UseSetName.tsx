import { useState } from "react";

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
      "Swimming",
      "Perplexed",
      "Howlin'",
      "Rolling",
      "Sticky",
      "Wounded",
      "Error",
    ];
    const Nouns: string[] = [
      "jumper",
      "Dennis",
      "dog",
      "Error",
      "bike",
      "bigfoot",
      "uncle",
      "head",
      "computer",
    ];

    const adjective = Adjectives[Math.floor(Math.random() * Adjectives.length)];
    const noun = Nouns[Math.floor(Math.random() * Nouns.length)];

    setName(`${adjective} ${noun}`);
  };

  function read(input: string) {
    setName(input);
  }

  return [name, generateRandom, read] as const;
}
