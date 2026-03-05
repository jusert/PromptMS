// 监听插件图标点击事件
chrome.action.onClicked.addListener((tab) => {
// 打开侧边栏
  chrome.sidePanel.setOptions({
    tabId: tab.id,
    path: 'index.html',
    enabled: true
  });
  chrome.sidePanel.open({ tabId: tab.id });
});

// 插件安装后默认在所有页面都能点击开启侧边栏
chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});