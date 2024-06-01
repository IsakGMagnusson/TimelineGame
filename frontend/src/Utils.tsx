export const clamp = function (min: number, value: number, max: number) {
  return Math.min(Math.max(value, min), max);
};

export const swapItemsInArray = function (index1: number, index2: number, arr: any[]) {
  const temp = arr[index1];
  arr[index1] = arr[index2];
  arr[index2] = temp;
  return arr;
};
