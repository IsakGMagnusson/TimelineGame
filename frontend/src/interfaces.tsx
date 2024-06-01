export interface CardData {
  question: string;
  date: number;
  state: number;
}

export interface Setting {
  description: string;
  query: string;
  type: string;
}

//TODO: fetch from backend
export enum Card_State {
  IN_PILE = 0,
  LOCKED = 1,
  ACTIVE = 2,
  PLACED = 3,
  REMOVED = 4,
  ANIMATE = 5,
}

export enum Class_Names {
  LOCKED = "square locked",
  ACTIVE = "square active",
  PLACED = "square placed",
  REMOVE_ACTIVE = "square active remove",
  REMOVE_PLACED = "square placed remove",
  ANIMATE = "square removed remove",
}
