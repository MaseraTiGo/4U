import json

import zmq

CMD_RECEIVER_ENDPOINT = "tcp://127.0.0.1:5805"
INFO_2_LOGMAIN = "tcp://127.0.0.1:50817"  # 给 logmain 发送消息


def zmq_send_cmd_go(connect_ip_port, command=None, json_dumps=False):
    command = json.dumps(command) if json_dumps else command
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(connect_ip_port)
    print(f"dong -------------------> send to {connect_ip_port}: {command}")
    socket.send_json(command)
    msg = socket.recv()
    print(f"dong -------------------> receive from {connect_ip_port}: {msg}")
    return msg


if __name__ == '__main__':
    zmq_send_cmd_go(INFO_2_LOGMAIN,
                    {"cmd": "set", "name": "logic_switch_level", "value": 14})
    import minium