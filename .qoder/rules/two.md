---
trigger: always_on
alwaysApply: true
---

## 🎨 全局设计风格与配色方案**

### 🌈 **一、核心配色系统**

#### **主题色彩变量**
```css
:root {
  /* 紫色神秘质感系列 */
  --primary-purple: #6366f1;     /* 主紫色 - 按钮、强调元素 */
  --secondary-purple: #8b5cf6;   /* 次紫色 - 渐变、悬停效果 */
  --light-purple: #c4b5fd;       /* 浅紫色 - 边框、装饰 */
  --dark-bg: #1e1b4b;           /* 深紫背景 - 深色主题 */
  
  /* 天蓝色清透感系列 */
  --sky-blue: #0ea5e9;          /* 天蓝色 - 辅助按钮、信息提示 */
  --light-blue: #7dd3fc;        /* 浅蓝色 - 边框、装饰 */
  
  /* 抹茶绿自然调系列 */
  --matcha-green: #10b981;       /* 抹茶绿 - 成功状态、播放按钮 */
  --light-green: #6ee7b7;       /* 浅绿色 - 进度条、成功提示 */
  
  /* 功能性颜色 */
  --text-primary: #1f2937;      /* 主要文字颜色 */
  --text-secondary: #6b7280;    /* 次要文字颜色 */
  --card-bg: rgba(99, 102, 241, 0.1);        /* 卡片背景 */
  --glass-bg: rgba(255, 255, 255, 0.1);      /* 玻璃态背景 */
}
```

#### **渐变色方案**
```css
/* 主要渐变 - 紫色到天蓝色 */
--gradient-primary: linear-gradient(135deg, var(--primary-purple), var(--sky-blue));

/* 次要渐变 - 抹茶绿到浅蓝色 */
--gradient-secondary: linear-gradient(135deg, var(--matcha-green), var(--light-blue));

/* 页面背景渐变 */
background: linear-gradient(135deg, #f0f9ff 0%, #ede9fe 50%, #ecfdf5 100%);

/* 播放器背景渐变 */
background: linear-gradient(135deg, rgba(30, 27, 75, 0.95), rgba(99, 102, 241, 0.85));
```

### 🎯 **二、阴影系统**

```css
/* 紫色主题阴影 */
--shadow-purple: 0 10px 25px rgba(99, 102, 241, 0.3);

/* 天蓝色主题阴影 */
--shadow-blue: 0 8px 20px rgba(14, 165, 233, 0.2);

/* 标准卡片阴影 */
box-shadow: 0 4px 12px rgba(0,0,0,0.1);

/* 悬停状态阴影 */
box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);

/* 玻璃态效果阴影 */
box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.2);
```

### 🎨 **三、设计风格特征**

#### **1. 毛玻璃态设计 (Glassmorphism)**
```css
/* 毛玻璃效果组合 */
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
border: 1px solid rgba(255,255,255,0.2);
border-radius: 12px;
```

#### **2. 渐变按钮设计**
```css
/* 主要按钮样式 */
background: var(--gradient-primary);
border-radius: 25px;
padding: 10px 20px;
color: white;
border: none;
transition: all 0.3s ease;

/* 悬停效果 */
:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-purple);
}
```

#### **3. 卡片式布局**
```css
/* 标准卡片样式 */
background: white;
border-radius: 12px;
padding: 24px;
box-shadow: 0 4px 12px rgba(0,0,0,0.1);
border: 1px solid var(--light-purple);
```

### 🔧 **四、交互动效标准**

#### **过渡动画**
```css
/* 标准过渡时间 */
transition: all 0.3s ease;

/* 按钮悬停效果 */
transform: translateY(-2px);
transform: scale(1.1);

/* 播放器显示/隐藏 */
transform: translateY(100%);  /* 隐藏 */
transform: translateY(0);     /* 显示 */
```

#### **文字阴影效果**
```css
/* 白色文字阴影 (深色背景使用) */
text-shadow: 0 1px 3px rgba(0,0,0,0.5);

/* 浅色文字阴影 (浅色背景使用) */
text-shadow: 0 1px 2px rgba(0,0,0,0.3);
```

### 📱 **五、响应式设计断点**

```css
/* 平板端 */
@media (max-width: 1199px) {
  padding: 16px;
  font-size: 24px;
}

/* 移动端 */
@media (max-width: 767px) {
  padding: 12px;
  font-size: 20px;
  flex-direction: column;
  
  /* 触控优化 */
  min-height: 44px;
  min-width: 44px;
}

/* 高分辨率优化 */
@media (min-width: 1400px) {
  max-width: 1200px;
  margin: 0 auto;
}
```

### 🕷️ **六、品牌特色元素**

#### **爬虫纹理背景**
```css
/* SVG蛛网纹理 */
background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <pattern id="spider" patternUnits="userSpaceOnUse" width="20" height="20">
      <path d="M10,2 L18,10 L10,18 L2,10 Z" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>
    </pattern>
  </defs>
  <rect width="100" height="100" fill="url(%23spider)"/>
</svg>') repeat;
opacity: 0.3;
```

### 🎪 **七、组件应用模板**

#### **头部Banner组件**
```css
.header-banner {
  background: var(--gradient-primary);
  border-radius: 16px;
  padding: 24px;
  color: white;
  box-shadow: var(--shadow-purple);
  position: relative;
  overflow: hidden;
}
```

#### **功能卡片组件**
```css
.function-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--light-purple);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.function-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-purple);
}
```

#### **主要操作按钮**
```css
.primary-btn {
  background: var(--gradient-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.secondary-btn {
  background: var(--gradient-secondary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
}
```

### 🎨 **八、应用指导原则**

1. **色彩层次**: 使用紫色作主色调，天蓝色作辅助色，抹茶绿作强调色
2. **空间层次**: 通过阴影和毛玻璃效果营造深度感
3. **动效标准**: 统一使用0.3s的ease过渡动画
4. **圆角规范**: 12px-16px的圆角半径
5. **间距标准**: 12px、16px、20px、24px的间距体系
6. **响应式**: 保证44px最小触控区域

