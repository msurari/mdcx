import time

from mdcx.config.manager import manager
from mdcx.i18n import tr
from mdcx.signals import signal_qt


def show_netstatus() -> None:
    signal_qt.show_net_info(time.strftime("%Y-%m-%d %H:%M:%S").center(80, "="))

    use_proxy, proxy, cf_bypass_url, cf_bypass_proxy, timeout, retry_count = (
        manager.config.use_proxy,
        manager.config.proxy,
        manager.config.cf_bypass_url,
        manager.config.cf_bypass_proxy,
        manager.config.timeout,
        manager.config.retry,
    )
    # display-only values: safe to translate (never compared against)
    bypass_status = tr("已配置") if cf_bypass_url else tr("未配置")
    bypass_proxy_status = tr("已配置") if cf_bypass_proxy else tr("未配置")

    if not use_proxy or not proxy:
        signal_qt.show_net_info(
            tr("当前网络状态") + "：❌ " + tr("未启用代理") + "\n"
            + "   " + tr("CF Bypass") + "：" + bypass_status
            + "    " + tr("Bypass代理") + "：" + bypass_proxy_status
            + "    " + tr("超时") + "：" + str(timeout)
            + "    " + tr("重试") + "：" + str(retry_count)
        )
    else:
        signal_qt.show_net_info(
            tr("当前网络状态") + "：✅ " + tr("已启用代理") + "\n"
            + "   " + tr("地址") + "：" + proxy + "\n"
            + "   " + tr("CF Bypass") + "：" + bypass_status
            + "    " + tr("Bypass代理") + "：" + bypass_proxy_status
            + "    " + tr("超时") + "：" + str(timeout)
            + "    " + tr("重试") + "：" + str(retry_count)
        )
    signal_qt.show_net_info("=" * 80)
