import { useState } from "react";

function useCount(initialCount: number = 0) {
  const [count, setCount] = useState(initialCount);

  const increment = () => {
    setCount(Math.min(30, count + 1));
  };

  const decrement = () => {
    setCount(Math.max(0, count - 1));
  };

  return {
    count,
    increment,
    decrement,
  };
}

export default useCount;
