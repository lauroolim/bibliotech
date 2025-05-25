from abc import ABC, abstractmethod
from app.models.employee import Employee
import logging

logger = logging.getLogger(__name__)

class IEmployeeRepository(ABC):
    @abstractmethod
    def fetch_employee_by_cpf(self, cpf: str) -> Employee:
        pass
    
    @abstractmethod
    def fetch_employee_by_id(self, employee_id: int) -> Employee:
        pass

class PSQLEmployeeRepository(IEmployeeRepository):
    def __init__(self, db):
        self.db = db

    def fetch_employee_by_cpf(self, cpf):
        query = "SELECT id, username, cpf, created_at, is_active, email, password FROM employees WHERE cpf = ?"
        params = [cpf]

        try:
            cursor = self.db.execute_query(query, params)
            employee = cursor.fetchone()

            if employee:
                return Employee(
                    id=employee[0],
                    username=employee[1], 
                    cpf=employee[2], 
                    created_at=employee[3],
                    is_active=employee[4],
                    email=employee[5],
                    password=employee[6]
                )
            return None
        except Exception as e:
            logger.error(f"Falha ao buscar funcionário por CPF: {str(e)}")
            return None

    def fetch_employee_by_id(self, employee_id):
        query = "SELECT id, username, cpf, created_at, is_active, email, password FROM employees WHERE id = ?"
        params = [int(employee_id)]  

        try:
            cursor = self.db.execute_query(query, params)
            employee = cursor.fetchone()

            if employee:
                return Employee(
                    id=employee[0],
                    username=employee[1], 
                    cpf=employee[2], 
                    created_at=employee[3],
                    is_active=employee[4],
                    email=employee[5],
                    password=employee[6]
                )
            return None
        except Exception as e:
            logger.error(f"Falha ao buscar funcionário por ID: {str(e)}")
            return None