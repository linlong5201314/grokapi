// Grok API 中转站 - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // 表格响应式处理
  const tables = document.querySelectorAll('.md-typeset table');
  tables.forEach(table => {
    if (!table.parentElement.classList.contains('table-wrapper')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'table-wrapper';
      wrapper.style.overflowX = 'auto';
      wrapper.style.margin = '1rem 0';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  // 页面滚动进度条
  const progressBar = document.createElement('div');
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--md-primary-fg-color);
    z-index: 9999;
    transition: width 0.3s ease;
    width: 0%;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (height > 0) {
      progressBar.style.width = (winScroll / height) * 100 + '%';
    }
  });

  // 搜索框中文占位符
  const searchInput = document.querySelector('.md-search__input');
  if (searchInput) {
    searchInput.setAttribute('placeholder', '搜索文档...');
  }

  // Ctrl/Cmd + K 快捷键聚焦搜索
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const input = document.querySelector('.md-search__input');
      if (input) input.focus();
    }
  });
});