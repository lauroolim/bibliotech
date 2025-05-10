import { Pool } from "pg";

export interface IUser {
  id: number;
  username: string;
  password: string;
  email: string;
  created_at: Date;
}

export interface IUserData {
  username: string;
  password: string;
  email: string;
}

export class User {
  db: Pool;

  constructor(db: Pool) {
    this.db = db;
  }

  async create({ username, password, email }: IUserData): Promise<IUser> {
    try {
      const result = await this.db.query<IUser>(
        "INSERT INTO users (username, password, email) VALUES ($1, $2, $3) RETURNING *",
        [username, password, email],
      );
      return result.rows[0];
    } catch (err) {
      console.error(err);
      throw new Error("erro ao cadastrar usuario" + err);
    }
  }
}
