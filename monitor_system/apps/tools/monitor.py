import psutil
from pprint import pprint  # 美化print
from datetime import datetime


class Monitor(object):
    def bytes2gb(self, data, key=""):
        """单位转化"""
        if key == "percent":
            return data
        return round(data / (1024 ** 3), 2)

    def cpu(self):
        """专门获取cpu的信息"""
        data = dict(
            # percpu True每个CPU的使用率 False 平均使用率
            # interval 1.平均 2.单独 3.物理cpu核心数 4.逻辑cpu核心数
            percent_avg=psutil.cpu_percent(interval=0, percpu=True),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_p=psutil.cpu_count(logical=False),
            num_l=psutil.cpu_count(logical=True)

        )
        return data

    def memory(self):
        """获取内存信息"""
        info = psutil.virtual_memory()
        data = dict(
            total=self.bytes2gb(info.total),
            used=self.bytes2gb(info.used),
            free=self.bytes2gb(info.free),
            percent=info.percent
        )
        return data

    def swap(self):
        """获取交换文件信息"""
        info = psutil.swap_memory()
        data = dict(
            total=self.bytes2gb(info.total),
            used=self.bytes2gb(info.used),
            free=self.bytes2gb(info.free),
            percent=info.percent
        )
        return data

    def disk(self):
        """获取磁盘信息"""
        info = psutil.disk_partitions()
        data = [
            dict(
                device=v.device,
                mountpoint=v.mountpoint,
                fstype=v.fstype,
                opts=v.opts,
                used={
                    k: self.bytes2gb(v)
                    for k, v in psutil.disk_usage(v.mountpoint)._asdict().items()
                }
            )
            for v in info
        ]
        return data

    def net(self):
        """获取网卡信息"""
        # 地址信息
        addrs = psutil.net_if_addrs()
        addrs_info = {
            k: [
                dict(
                    family=val.family.name,
                    address=val.address,
                    netmask=val.netmask,
                    broadcast=val.broadcast
                )
                for val in v if val.family.name == "AF_INET"
            ][0]
            for k, v in addrs.items()
        }
        # 获取输入输出信息（收发包,字节)
        io = psutil.net_io_counters(pernic=True)
        data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **addrs_info[k]
            )
            for k, v in io.items()
        ]
        return data

    def lastest_start_time(self):
        """获取其最近开机时间"""
        date = datetime.fromtimestamp(psutil.boot_time())
        date = date.strftime("%Y-%m-%d-%H:%M:%S")
        return date

    def logined_user(self):
        """获取系统登录用户"""
        users = psutil.users()
        data = [
            dict(
                name=v.name,
                terminal=v.terminal,
                host=v.host,
                started=datetime.fromtimestamp(v.started).strftime("%Y-%m-%d-%H:%M:%S"),
                pid=v.pid,
            )
            for v in users
        ]
        return data


if __name__ == '__main__':
    m = Monitor()
    print(m.cpu())
    # print(m.memory())
    # pprint(m.logined_user())
