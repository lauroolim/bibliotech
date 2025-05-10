import { Router } from "express";
import { UserController } from "../controllers/users.controller";

const rt = Router();
const userController = new UserController();

rt.get("admin/form/add-users", (req, res) =>
  userController.displayFormAddUser(res),
);
rt.post("", (req, res) => userController.insertUser(req, res));

export default rt;
