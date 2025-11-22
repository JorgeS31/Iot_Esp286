from flask import Blueprint, jsonify, request
from models.iot_device import IotDeviceModel
import ipaddress

iot_devices_bp = Blueprint("iot_devices", __name__, url_prefix="/api/iot-devices")


def _validate_payload(data: dict):
    errors = []
    name = (data.get("name") or "").strip()
    ip = (data.get("ip") or "").strip()
    status_texto = (data.get("status_texto") or "").strip()
    status_clave = data.get("status_clave")

    if not name or len(name) > 30:
        errors.append("name es requerido y debe tener máximo 30 caracteres.")
    if not ip or len(ip) > 15:
        errors.append("ip es requerida y debe tener máximo 15 caracteres.")
    else:
        try:
            ipaddress.IPv4Address(ip)
        except Exception:
            errors.append("ip debe ser una dirección IPv4 válida.")
    if status_clave is None:
        errors.append("status_clave es requerido.")
    else:
        try:
            sc = int(status_clave)
            if sc < 0 or sc > 99:
                errors.append("status_clave debe estar en el rango 0–99.")
        except Exception:
            errors.append("status_clave debe ser entero.")
    if not status_texto or len(status_texto) > 25:
        errors.append("status_texto es requerido y debe tener máximo 25 caracteres.")
    return errors


@iot_devices_bp.route("/", methods=["GET"])
def get_all():
    try:
        data = IotDeviceModel.select_all()
        return jsonify({"success": True, "count": len(data), "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@iot_devices_bp.route("/last5", methods=["GET"])
def get_last5():
    try:
        data = IotDeviceModel.select_last5()
        return jsonify({"success": True, "count": len(data), "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@iot_devices_bp.route("/last-status-texto", methods=["GET"])
def get_last_status_texto():
    try:
        value = IotDeviceModel.get_last_status_texto()
        return jsonify({"success": True, "status_texto": value}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@iot_devices_bp.route("/", methods=["POST"])
def create_device():
    try:
        data = request.get_json(silent=True) or {}
        errors = _validate_payload(data)
        if errors:
            return jsonify({"success": False, "errors": errors}), 400
        new_id = IotDeviceModel.insert(
            name=data["name"].strip(),
            ip=data["ip"].strip(),
            status_clave=int(data["status_clave"]),
            status_texto=data["status_texto"].strip()
        )
        return jsonify({"success": True, "new_id": new_id}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
