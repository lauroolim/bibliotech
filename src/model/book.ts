import { Pool } from "pg";

export interface IBook {
  id: number;
  title: string;
  author: string;
  created_at: Date;
}

export class Book {
  db: Pool;

  constructor(db: Pool) {
    this.db = db;
  }

  async getAll(): Promise<IBook[]> {
    try {
      const result = await this.db.query("SELECT * FROM books ORDER BY id");
      return result.rows;
    } catch (err) {
      console.error(err);
      throw new Error("erro ao buscar livros" + err);
    }
  }

  async create(title: string, author: string): Promise<IBook> {
    try {
      const result = await this.db.query(
        "INSERT INTO books (title, author) VALUES ($1, $2) RETURNING *",
        [title, author],
      );
      return result.rows[0];
    } catch (err) {
      throw new Error("erro ao cadastrar livros" + err);
    }
  }

  async getOne(id: number): Promise<IBook | null> {
    try {
      const result = await this.db.query("SELECT * FROM books WHERE id = ?", [
        id,
      ]);
      return result.rows[0];
    } catch (err) {
      throw new Error("erro ao buscar livro" + err);
    }
  }
}
