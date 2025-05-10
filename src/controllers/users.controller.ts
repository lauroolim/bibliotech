import { IUserData, User } from "../model/user";
import { Request, Response } from "express";
import { pool } from "../../db";

export class UserController {
  private user: User;

  constructor() {
    this.user = new User(pool);
  }

  async displayFormAddUser(res: Response) {
    try {
      res.render("admin/add-user");
    } catch (err) {
      console.error(
        "erro no display do formulario de adicionar novos usuarios " + err,
      );
      res.status(500).render("error", {
        message:
          "Erro interno do servidor ao renderizar formulario de adicionar usuarios, tente mais tarde...",
      });
    }
  }

  async insertUser(req: Request, res: Response) {
    try {
      if (!req.body) {
        return res.status(400).render("error", {
          message: "Nenhum dado foi recebido",
        });
      }
      const userData: IUserData = req.body;

      const insert = await this.user.create(userData);
      res.redirect("/admin/add-user");
    } catch (err) {
      console.error("falha ao inserir novo usuario " + err);
      res.sendStatus(500).render("error", {
        message:
          "Erro interno do servidor ao inserir novo usuario, tente mais tarde...",
      });
    }
  }
}
