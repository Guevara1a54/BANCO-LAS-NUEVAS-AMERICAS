from dao.beneficiario_dao import BeneficiarioDAO
from modelos.beneficiario import Beneficiario


class BeneficiarioControlador:
    @classmethod
    def registrar(cls, idBeneficiario: str, nombres: str, apellidos: str, numeroCuenta: str, bancoDestino: str) -> bool:
        beneficiario = Beneficiario(idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino)
        return BeneficiarioDAO.insertar(beneficiario) > 0

    @classmethod
    def listar(cls) -> list[Beneficiario]:
        return BeneficiarioDAO.seleccionar()

    @classmethod
    def buscar(cls, idBeneficiario: str) -> Beneficiario | None:
        return BeneficiarioDAO.buscar_por_id(idBeneficiario)

    @classmethod
    def modificar(cls, idBeneficiario: str, nombres: str, apellidos: str, numeroCuenta: str, bancoDestino: str) -> bool:
        beneficiario = Beneficiario(idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino)
        return BeneficiarioDAO.actualizar(beneficiario) > 0

    @classmethod
    def eliminar(cls, idBeneficiario: str) -> bool:
        return BeneficiarioDAO.eliminar(idBeneficiario) > 0
