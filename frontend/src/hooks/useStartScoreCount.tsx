import { useState } from "react";

function useStartScoreCount(initialCount: number = 0) {
  const [count, setCount] = useState(initialCount);

  const increment = () => {
    setCount(Math.min(30, count + 1));
  };

  const minScore = 2;
  const decrement = () => {
    setCount(Math.max(minScore, count - 1));
  };

  return {
    count,
    increment,
    decrement,
  };
}

export default useStartScoreCount;
