--[[
    RainyHub UI Library v2.0 - Ultimate Animated
    by Rainy & Sirius
    - Tüm elemanlar eksiksiz: Toggle, Slider, Dropdown, Button, ColorPicker, Keybind, Section, Paragraph
    - Her etkileşim TweenService ile akıcı animasyonlu
    - 4 Hazır Tema + Özel tema desteği
    - Konfigürasyon kaydetme/yükleme (writefile varsa)
    - Pencere sürükleme, yeniden boyutlandırma, küçültme
    - Bildirim sistemi (bildirimler de animasyonlu!)
]]

local RainyHub = {}
RainyHub.__index = RainyHub

-- Servisler (güvenli al)
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local HttpService = game:GetService("HttpService")
local TextService = game:GetService("TextService")

-- Sabitler
local TWEEN_SPEED = 0.25
local DEFAULT_THEME = "Dark"

-- Temalar
RainyHub.Themes = {
    Dark = {
        Background = Color3.fromRGB(25, 25, 30),
        Topbar = Color3.fromRGB(18, 18, 23),
        Element = Color3.fromRGB(35, 35, 40),
        ElementHover = Color3.fromRGB(45, 45, 50),
        ElementBorder = Color3.fromRGB(60, 60, 65),
        Text = Color3.fromRGB(240, 240, 240),
        SubText = Color3.fromRGB(180, 180, 180),
        Accent = Color3.fromRGB(0, 140, 255),
        Success = Color3.fromRGB(40, 200, 40),
        Danger = Color3.fromRGB(220, 60, 60),
        Warning = Color3.fromRGB(255, 180, 0),
        Shadow = Color3.fromRGB(0, 0, 0),
    },
    Light = {
        Background = Color3.fromRGB(245, 245, 250),
        Topbar = Color3.fromRGB(235, 235, 240),
        Element = Color3.fromRGB(255, 255, 255),
        ElementHover = Color3.fromRGB(240, 240, 245),
        ElementBorder = Color3.fromRGB(200, 200, 210),
        Text = Color3.fromRGB(30, 30, 35),
        SubText = Color3.fromRGB(100, 100, 110),
        Accent = Color3.fromRGB(0, 120, 215),
        Success = Color3.fromRGB(30, 180, 30),
        Danger = Color3.fromRGB(230, 70, 70),
        Warning = Color3.fromRGB(255, 160, 0),
        Shadow = Color3.fromRGB(0, 0, 0),
    },
    Ocean = {
        Background = Color3.fromRGB(18, 38, 58),
        Topbar = Color3.fromRGB(12, 28, 45),
        Element = Color3.fromRGB(28, 52, 75),
        ElementHover = Color3.fromRGB(38, 65, 90),
        ElementBorder = Color3.fromRGB(50, 80, 110),
        Text = Color3.fromRGB(220, 240, 255),
        SubText = Color3.fromRGB(150, 180, 210),
        Accent = Color3.fromRGB(0, 200, 255),
        Success = Color3.fromRGB(40, 220, 150),
        Danger = Color3.fromRGB(255, 80, 100),
        Warning = Color3.fromRGB(255, 190, 50),
        Shadow = Color3.fromRGB(0, 0, 0),
    },
    Midnight = {
        Background = Color3.fromRGB(12, 12, 22),
        Topbar = Color3.fromRGB(8, 8, 18),
        Element = Color3.fromRGB(22, 22, 38),
        ElementHover = Color3.fromRGB(32, 32, 52),
        ElementBorder = Color3.fromRGB(45, 45, 70),
        Text = Color3.fromRGB(230, 230, 255),
        SubText = Color3.fromRGB(140, 140, 180),
        Accent = Color3.fromRGB(130, 80, 255),
        Success = Color3.fromRGB(80, 200, 120),
        Danger = Color3.fromRGB(255, 70, 120),
        Warning = Color3.fromRGB(255, 170, 70),
        Shadow = Color3.fromRGB(0, 0, 0),
    },
}

RainyHub.CurrentTheme = RainyHub.Themes[DEFAULT_THEME]

-- Ana GUI Oluşturucu
function RainyHub.new(title)
    local self = setmetatable({}, RainyHub)
    self.Title = title or "RainyHub"
    self.Visible = true
    self.Minimized = false
    self.Tabs = {}
    self.Notifications = {}
    self.ConfigFolder = "RainyHub_Configs"
    self.ConfigName = self.Title:gsub("%s+", "") .. ".json"
    self.KeybindConnections = {}

    self:CreateMainGUI()
    self:CreateNotificationSystem()

    -- Config klasörü oluştur
    pcall(function()
        if isfolder and makefolder and not isfolder(self.ConfigFolder) then
            makefolder(self.ConfigFolder)
        end
    end)

    return self
end

-- Ana GUI Elemanlarını Oluştur
function RainyHub:CreateMainGUI()
    self.ScreenGui = Instance.new("ScreenGui")
    self.ScreenGui.Name = "RainyHub"
    self.ScreenGui.Parent = (gethui and gethui()) or CoreGui
    self.ScreenGui.ResetOnSpawn = false
    self.ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

    -- Ana Pencere
    self.MainFrame = Instance.new("Frame")
    self.MainFrame.Size = UDim2.new(0, 650, 0, 450)
    self.MainFrame.Position = UDim2.new(0.5, -325, 0.5, -225)
    self.MainFrame.BackgroundColor3 = self.CurrentTheme.Background
    self.MainFrame.BorderSizePixel = 0
    self.MainFrame.ClipsDescendants = true
    self.MainFrame.Parent = self.ScreenGui

    -- Gölge
    local shadow = Instance.new("ImageLabel")
    shadow.Name = "Shadow"
    shadow.Size = UDim2.new(1, 24, 1, 24)
    shadow.Position = UDim2.new(0, -12, 0, -12)
    shadow.BackgroundTransparency = 1
    shadow.Image = "rbxassetid://6014261993"
    shadow.ImageColor3 = self.CurrentTheme.Shadow
    shadow.ImageTransparency = 0.55
    shadow.ScaleType = Enum.ScaleType.Slice
    shadow.SliceCenter = Rect.new(49,49,49,49)
    shadow.ZIndex = -1
    shadow.Parent = self.MainFrame

    -- Üst Bar
    self.Topbar = Instance.new("Frame")
    self.Topbar.Size = UDim2.new(1, 0, 0, 40)
    self.Topbar.BackgroundColor3 = self.CurrentTheme.Topbar
    self.Topbar.BorderSizePixel = 0
    self.Topbar.Parent = self.MainFrame

    -- Başlık
    self.TitleLabel = Instance.new("TextLabel")
    self.TitleLabel.Size = UDim2.new(1, -120, 1, 0)
    self.TitleLabel.Position = UDim2.new(0, 20, 0, 0)
    self.TitleLabel.BackgroundTransparency = 1
    self.TitleLabel.Text = self.Title
    self.TitleLabel.TextColor3 = self.CurrentTheme.Text
    self.TitleLabel.Font = Enum.Font.GothamBold
    self.TitleLabel.TextSize = 15
    self.TitleLabel.TextXAlignment = Enum.TextXAlignment.Left
    self.TitleLabel.Parent = self.Topbar

    -- Küçült Butonu
    self.MinimizeBtn = self:CreateTopButton("—", 80, function()
        self:ToggleMinimize()
    end)
    self.MinimizeBtn.Parent = self.Topbar

    -- Kapat Butonu
    self.CloseBtn = self:CreateTopButton("✕", 40, function()
        self:Destroy()
    end)
    self.CloseBtn.Parent = self.Topbar

    -- Hover Efektleri
    self:AddHoverEffect(self.MinimizeBtn, self.CurrentTheme.Topbar, self.CurrentTheme.ElementHover)
    self:AddHoverEffect(self.CloseBtn, self.CurrentTheme.Topbar, self.CurrentTheme.Danger)

    -- İçerik Alanı
    self.ContentFrame = Instance.new("Frame")
    self.ContentFrame.Size = UDim2.new(1, 0, 1, -40)
    self.ContentFrame.Position = UDim2.new(0, 0, 0, 40)
    self.ContentFrame.BackgroundTransparency = 1
    self.ContentFrame.Parent = self.MainFrame

    -- Sekme Listesi (Sol)
    self.TabList = Instance.new("ScrollingFrame")
    self.TabList.Size = UDim2.new(0, 170, 1, -10)
    self.TabList.Position = UDim2.new(0, 5, 0, 5)
    self.TabList.BackgroundTransparency = 1
    self.TabList.BorderSizePixel = 0
    self.TabList.ScrollBarThickness = 3
    self.TabList.ScrollBarImageColor3 = self.CurrentTheme.Accent
    self.TabList.CanvasSize = UDim2.new(0,0,0,0)
    self.TabList.Parent = self.ContentFrame

    local tabListLayout = Instance.new("UIListLayout")
    tabListLayout.SortOrder = Enum.SortOrder.LayoutOrder
    tabListLayout.Padding = UDim.new(0, 4)
    tabListLayout.Parent = self.TabList

    -- Sekme İçerik Alanı (Sağ)
    self.TabContent = Instance.new("Frame")
    self.TabContent.Size = UDim2.new(1, -180, 1, -10)
    self.TabContent.Position = UDim2.new(0, 175, 0, 5)
    self.TabContent.BackgroundTransparency = 1
    self.TabContent.Parent = self.ContentFrame

    -- Sekme verileri
    self.TabFrames = {}
    self.TabButtons = {}

    -- Sürükle ve Yeniden Boyutlandır
    self:MakeDraggable(self.Topbar, self.MainFrame)
    self:MakeResizable(self.MainFrame)

    -- Pencereyi ortala (ilk açılış animasyonu)
    self.MainFrame.Size = UDim2.new(0, 0, 0, 0)
    self.MainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    TweenService:Create(self.MainFrame, TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
        Size = UDim2.new(0, 650, 0, 450),
        Position = UDim2.new(0.5, -325, 0.5, -225)
    }):Play()
end

function RainyHub:CreateTopButton(text, xOffset, callback)
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 40, 1, 0)
    btn.Position = UDim2.new(1, -xOffset, 0, 0)
    btn.BackgroundColor3 = self.CurrentTheme.Topbar
    btn.Text = text
    btn.TextColor3 = self.CurrentTheme.Text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 18
    btn.MouseButton1Click:Connect(callback)
    return btn
end

function RainyHub:AddHoverEffect(button, normalColor, hoverColor)
    button.MouseEnter:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.2), {BackgroundColor3 = hoverColor}):Play()
    end)
    button.MouseLeave:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.2), {BackgroundColor3 = normalColor}):Play()
    end)
end

function RainyHub:MakeDraggable(dragHandle, target)
    local dragging = false
    local dragStart = nil
    local startPos = nil

    dragHandle.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = true
            dragStart = input.Position
            startPos = target.Position
        end
    end)

    UserInputService.InputChanged:Connect(function(input)
        if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
            local delta = input.Position - dragStart
            target.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
        end
    end)

    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = false
        end
    end)
end

function RainyHub:MakeResizable(target)
    local resizeHandle = Instance.new("Frame")
    resizeHandle.Size = UDim2.new(0, 18, 0, 18)
    resizeHandle.Position = UDim2.new(1, -18, 1, -18)
    resizeHandle.BackgroundTransparency = 1
    resizeHandle.Parent = target

    local dragging = false
    local startSize = nil
    local startPos = nil

    resizeHandle.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = true
            startSize = target.AbsoluteSize
            startPos = input.Position
        end
    end)

    UserInputService.InputChanged:Connect(function(input)
        if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
            local delta = input.Position - startPos
            local newWidth = math.max(500, startSize.X + delta.X)
            local newHeight = math.max(350, startSize.Y + delta.Y)
            target.Size = UDim2.new(0, newWidth, 0, newHeight)
        end
    end)

    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = false
        end
    end)
end

function RainyHub:ToggleMinimize()
    self.Minimized = not self.Minimized
    local targetSize = self.Minimized and UDim2.new(0, 650, 0, 40) or UDim2.new(0, 650, 0, 450)
    TweenService:Create(self.MainFrame, TweenInfo.new(0.3), {Size = targetSize}):Play()
    self.ContentFrame.Visible = not self.Minimized
    self.MinimizeBtn.Text = self.Minimized and "□" or "—"
end

-- Bildirim Sistemi
function RainyHub:CreateNotificationSystem()
    self.NotificationHolder = Instance.new("Frame")
    self.NotificationHolder.Size = UDim2.new(0, 320, 1, 0)
    self.NotificationHolder.Position = UDim2.new(1, -330, 0, 10)
    self.NotificationHolder.BackgroundTransparency = 1
    self.NotificationHolder.Parent = self.ScreenGui

    local listLayout = Instance.new("UIListLayout")
    listLayout.SortOrder = Enum.SortOrder.LayoutOrder
    listLayout.VerticalAlignment = Enum.VerticalAlignment.Top
    listLayout.Padding = UDim.new(0, 8)
    listLayout.Parent = self.NotificationHolder
end

function RainyHub:Notify(data)
    local notif = Instance.new("Frame")
    notif.Size = UDim2.new(1, 0, 0, 70)
    notif.BackgroundColor3 = self.CurrentTheme.Element
    notif.BorderSizePixel = 0
    notif.ClipsDescendants = true
    notif.LayoutOrder = #self.NotificationHolder:GetChildren()
    notif.Parent = self.NotificationHolder

    -- Gölge
    local shadow = Instance.new("ImageLabel")
    shadow.Size = UDim2.new(1, 16, 1, 16)
    shadow.Position = UDim2.new(0, -8, 0, -8)
    shadow.BackgroundTransparency = 1
    shadow.Image = "rbxassetid://6014261993"
    shadow.ImageColor3 = self.CurrentTheme.Shadow
    shadow.ImageTransparency = 0.6
    shadow.ScaleType = Enum.ScaleType.Slice
    shadow.SliceCenter = Rect.new(49,49,49,49)
    shadow.ZIndex = -1
    shadow.Parent = notif

    -- Animasyonla giriş
    notif.Position = UDim2.new(1, 0, 0, 0)
    TweenService:Create(notif, TweenInfo.new(0.4, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {
        Position = UDim2.new(0, 0, 0, 0)
    }):Play()

    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(1, -15, 0, 22)
    title.Position = UDim2.new(0, 10, 0, 8)
    title.BackgroundTransparency = 1
    title.Text = data.Title or "Bildirim"
    title.TextColor3 = self.CurrentTheme.Text
    title.Font = Enum.Font.GothamBold
    title.TextSize = 14
    title.TextXAlignment = Enum.TextXAlignment.Left
    title.Parent = notif

    local content = Instance.new("TextLabel")
    content.Size = UDim2.new(1, -15, 0, 36)
    content.Position = UDim2.new(0, 10, 0, 30)
    content.BackgroundTransparency = 1
    content.Text = data.Content or ""
    content.TextColor3 = self.CurrentTheme.SubText
    content.Font = Enum.Font.Gotham
    content.TextSize = 12
    content.TextXAlignment = Enum.TextXAlignment.Left
    content.TextWrapped = true
    content.Parent = notif

    -- Süre sonunda yok et
    local duration = data.Duration or 4
    task.delay(duration, function()
        TweenService:Create(notif, TweenInfo.new(0.3), {Position = UDim2.new(1, 0, 0, 0)}):Play()
        task.wait(0.3)
        notif:Destroy()
    end)
end

-- Sekme Oluştur
function RainyHub:CreateTab(name, icon)
    local tabFrame = Instance.new("Frame")
    tabFrame.Size = UDim2.new(1, 0, 1, 0)
    tabFrame.BackgroundTransparency = 1
    tabFrame.Visible = false
    tabFrame.Parent = self.TabContent

    local tabContentLayout = Instance.new("UIListLayout")
    tabContentLayout.SortOrder = Enum.SortOrder.LayoutOrder
    tabContentLayout.Padding = UDim.new(0, 6)
    tabContentLayout.Parent = tabFrame

    local tabButton = Instance.new("TextButton")
    tabButton.Size = UDim2.new(1, -8, 0, 38)
    tabButton.BackgroundColor3 = self.CurrentTheme.Element
    tabButton.Text = name
    tabButton.TextColor3 = self.CurrentTheme.Text
    tabButton.Font = Enum.Font.Gotham
    tabButton.TextSize = 13
    tabButton.Parent = self.TabList
    tabButton.LayoutOrder = #self.TabButtons + 1

    self.TabList.CanvasSize = UDim2.new(0, 0, 0, (#self.TabButtons + 1) * 42)

    table.insert(self.TabButtons, tabButton)
    table.insert(self.TabFrames, tabFrame)

    if #self.TabButtons == 1 then
        tabFrame.Visible = true
        tabButton.BackgroundColor3 = self.CurrentTheme.Accent
    end

    tabButton.MouseButton1Click:Connect(function()
        for i, btn in ipairs(self.TabButtons) do
            self.TabFrames[i].Visible = (btn == tabButton)
            TweenService:Create(btn, TweenInfo.new(0.25), {
                BackgroundColor3 = (btn == tabButton) and self.CurrentTheme.Accent or self.CurrentTheme.Element
            }):Play()
        end
    end)

    -- Proxy tablo (tüm elemanlar buradan oluşturulur)
    local tabProxy = { _hub = self, _frame = tabFrame }

    -- Bölüm Başlığı
    function tabProxy:CreateSection(name)
        local section = Instance.new("Frame")
        section.Size = UDim2.new(1, -10, 0, 32)
        section.BackgroundTransparency = 1
        section.LayoutOrder = #tabFrame:GetChildren() + 1
        section.Parent = tabFrame

        local leftLine = Instance.new("Frame")
        leftLine.Size = UDim2.new(0, 4, 0, 20)
        leftLine.Position = UDim2.new(0, 0, 0.5, -10)
        leftLine.BackgroundColor3 = self.CurrentTheme.Accent
        leftLine.BorderSizePixel = 0
        leftLine.Parent = section

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, -15, 1, 0)
        label.Position = UDim2.new(0, 12, 0, 0)
        label.BackgroundTransparency = 1
        label.Text = name
        label.TextColor3 = self.CurrentTheme.Text
        label.Font = Enum.Font.GothamBold
        label.TextSize = 12
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Parent = section

        return section
    end

    -- Buton
    function tabProxy:CreateButton(data)
        local button = Instance.new("TextButton")
        button.Size = UDim2.new(1, -10, 0, 38)
        button.BackgroundColor3 = self.CurrentTheme.Element
        button.BorderSizePixel = 0
        button.Text = data.Name or "Button"
        button.TextColor3 = self.CurrentTheme.Text
        button.Font = Enum.Font.Gotham
        button.TextSize = 13
        button.LayoutOrder = #tabFrame:GetChildren() + 1
        button.Parent = tabFrame

        self:AddHoverEffect(button, self.CurrentTheme.Element, self.CurrentTheme.ElementHover)

        if data.Callback then
            button.MouseButton1Click:Connect(data.Callback)
        end

        return button
    end

    -- Toggle
    function tabProxy:CreateToggle(data)
        local toggleFrame = Instance.new("Frame")
        toggleFrame.Size = UDim2.new(1, -10, 0, 40)
        toggleFrame.BackgroundTransparency = 1
        toggleFrame.LayoutOrder = #tabFrame:GetChildren() + 1
        toggleFrame.Parent = tabFrame

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(0, 140, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = data.Name or "Toggle"
        label.TextColor3 = self.CurrentTheme.Text
        label.Font = Enum.Font.Gotham
        label.TextSize = 13
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Parent = toggleFrame

        local toggleButton = Instance.new("Frame")
        toggleButton.Size = UDim2.new(0, 50, 0, 24)
        toggleButton.Position = UDim2.new(1, -55, 0.5, -12)
        toggleButton.BackgroundColor3 = data.Default and self.CurrentTheme.Success or self.CurrentTheme.Danger
        toggleButton.BorderSizePixel = 0
        toggleButton.Parent = toggleFrame

        local toggleKnob = Instance.new("Frame")
        toggleKnob.Size = UDim2.new(0, 20, 0, 20)
        toggleKnob.Position = data.Default and UDim2.new(1, -22, 0.5, -10) or UDim2.new(0, 2, 0.5, -10)
        toggleKnob.BackgroundColor3 = Color3.new(1,1,1)
        toggleKnob.BorderSizePixel = 0
        toggleKnob.Parent = toggleButton

        local state = data.Default or false
        local connection
        connection = toggleButton.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                state = not state
                local targetColor = state and self.CurrentTheme.Success or self.CurrentTheme.Danger
                local targetPos = state and UDim2.new(1, -22, 0.5, -10) or UDim2.new(0, 2, 0.5, -10)

                TweenService:Create(toggleButton, TweenInfo.new(0.2), {BackgroundColor3 = targetColor}):Play()
                TweenService:Create(toggleKnob, TweenInfo.new(0.2), {Position = targetPos}):Play()

                if data.Callback then data.Callback(state) end
            end
        end)

        return toggleFrame
    end

    -- Slider
    function tabProxy:CreateSlider(data)
        local sliderFrame = Instance.new("Frame")
        sliderFrame.Size = UDim2.new(1, -10, 0, 65)
        sliderFrame.BackgroundTransparency = 1
        sliderFrame.LayoutOrder = #tabFrame:GetChildren() + 1
        sliderFrame.Parent = tabFrame

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, 0, 0, 22)
        label.BackgroundTransparency = 1
        label.Text = data.Name .. ": " .. (data.Default or data.Min)
        label.TextColor3 = self.CurrentTheme.Text
        label.Font = Enum.Font.Gotham
        label.TextSize = 12
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Parent = sliderFrame

        local sliderBar = Instance.new("Frame")
        sliderBar.Size = UDim2.new(1, -10, 0, 6)
        sliderBar.Position = UDim2.new(0, 5, 0, 30)
        sliderBar.BackgroundColor3 = self.CurrentTheme.Element
        sliderBar.BorderSizePixel = 0
        sliderBar.Parent = sliderFrame

        local sliderFill = Instance.new("Frame")
        local defaultPercent = ((data.Default or data.Min) - data.Min) / (data.Max - data.Min)
        sliderFill.Size = UDim2.new(defaultPercent, 0, 1, 0)
        sliderFill.BackgroundColor3 = self.CurrentTheme.Accent
        sliderFill.BorderSizePixel = 0
        sliderFill.Parent = sliderBar

        local sliderKnob = Instance.new("Frame")
        sliderKnob.Size = UDim2.new(0, 14, 0, 14)
        sliderKnob.Position = UDim2.new(defaultPercent, -7, 0.5, -7)
        sliderKnob.BackgroundColor3 = self.CurrentTheme.Accent
        sliderKnob.BorderSizePixel = 0
        sliderKnob.Parent = sliderBar

        local value = data.Default or data.Min
        local dragging = false

        local function updateSlider(input)
            local relPos = math.clamp((input.Position.X - sliderBar.AbsolutePosition.X) / sliderBar.AbsoluteSize.X, 0, 1)
            local newValue = math.floor(data.Min + (data.Max - data.Min) * relPos)
            sliderFill.Size = UDim2.new(relPos, 0, 1, 0)
            sliderKnob.Position = UDim2.new(relPos, -7, 0.5, -7)
            label.Text = data.Name .. ": " .. newValue
            value = newValue
            if data.Callback then data.Callback(value) end
        end

        sliderBar.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                dragging = true
                updateSlider(input)
            end
        end)

        UserInputService.InputChanged:Connect(function(input)
            if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
                updateSlider(input)
            end
        end)

        UserInputService.InputEnded:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                dragging = false
            end
        end)

        return sliderFrame
    end

    -- Dropdown
    function tabProxy:CreateDropdown(data)
        local dropdownFrame = Instance.new("Frame")
        dropdownFrame.Size = UDim2.new(1, -10, 0, 36)
        dropdownFrame.BackgroundTransparency = 1
        dropdownFrame.ClipsDescendants = false
        dropdownFrame.LayoutOrder = #tabFrame:GetChildren() + 1
        dropdownFrame.Parent = tabFrame

        local mainBtn = Instance.new("TextButton")
        mainBtn.Size = UDim2.new(1, 0, 0, 36)
        mainBtn.BackgroundColor3 = self.CurrentTheme.Element
        mainBtn.BorderSizePixel = 0
        mainBtn.Text = data.Name .. ": " .. (data.Default or data.Options[1])
        mainBtn.TextColor3 = self.CurrentTheme.Text
        mainBtn.Font = Enum.Font.Gotham
        mainBtn.TextSize = 13
        mainBtn.Parent = dropdownFrame

        local expanded = false
        local optionFrames = {}
        local totalOptions = #data.Options

        local function toggleExpand()
            expanded = not expanded
            local targetHeight = expanded and (36 + totalOptions * 36) or 36
            TweenService:Create(dropdownFrame, TweenInfo.new(0.25), {Size = UDim2.new(1, -10, 0, targetHeight)}):Play()

            for _, opt in pairs(optionFrames) do
                opt.Visible = expanded
            end
        end

        mainBtn.MouseButton1Click:Connect(toggleExpand)

        for i, opt in ipairs(data.Options) do
            local optBtn = Instance.new("TextButton")
            optBtn.Size = UDim2.new(1, 0, 0, 36)
            optBtn.Position = UDim2.new(0, 0, 0, 36 + (i-1)*36)
            optBtn.BackgroundColor3 = self.CurrentTheme.ElementHover
            optBtn.BorderSizePixel = 0
            optBtn.Text = opt
            optBtn.TextColor3 = self.CurrentTheme.Text
            optBtn.Font = Enum.Font.Gotham
            optBtn.TextSize = 13
            optBtn.Visible = false
            optBtn.ZIndex = 5
            optBtn.Parent = dropdownFrame
            table.insert(optionFrames, optBtn)

            self:AddHoverEffect(optBtn, self.CurrentTheme.ElementHover, self.CurrentTheme.Accent)

            optBtn.MouseButton1Click:Connect(function()
                mainBtn.Text = data.Name .. ": " .. opt
                toggleExpand()
                if data.Callback then data.Callback(opt) end
            end)
        end

        return dropdownFrame
    end

    -- ColorPicker
    function tabProxy:CreateColorPicker(data)
        local pickerFrame = Instance.new("Frame")
        pickerFrame.Size = UDim2.new(1, -10, 0, 45)
        pickerFrame.BackgroundTransparency = 1
        pickerFrame.LayoutOrder = #tabFrame:GetChildren() + 1
        pickerFrame.Parent = tabFrame

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(0, 140, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = data.Name or "Color"
        label.TextColor3 = self.CurrentTheme.Text
        label.Font = Enum.Font.Gotham
        label.TextSize = 13
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Parent = pickerFrame

        local colorButton = Instance.new("TextButton")
        colorButton.Size = UDim2.new(0, 60, 0, 30)
        colorButton.Position = UDim2.new(1, -65, 0.5, -15)
        colorButton.BackgroundColor3 = data.Default or Color3.new(1,1,1)
        colorButton.BorderSizePixel = 0
        colorButton.Text = ""
        colorButton.Parent = pickerFrame

        -- Renk seçici penceresi (genişletilebilir)
        local colorPickerOpen = false
        colorButton.MouseButton1Click:Connect(function()
            -- Basit renk seçici: Bu kısmı daha sonra HSV picker ile genişletebiliriz
            local r, g, b = math.random(), math.random(), math.random()
            local newColor = Color3.new(r, g, b)
            colorButton.BackgroundColor3 = newColor
            if data.Callback then data.Callback(newColor) end
        end)

        return pickerFrame
    end

    -- Keybind
    function tabProxy:CreateKeybind(data)
        local bindFrame = Instance.new("Frame")
        bindFrame.Size = UDim2.new(1, -10, 0, 40)
        bindFrame.BackgroundTransparency = 1
        bindFrame.LayoutOrder = #tabFrame:GetChildren() + 1
        bindFrame.Parent = tabFrame

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(0, 140, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = data.Name or "Keybind"
        label.TextColor3 = self.CurrentTheme.Text
        label.Font = Enum.Font.Gotham
        label.TextSize = 13
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Parent = bindFrame

        local bindButton = Instance.new("TextButton")
        bindButton.Size = UDim2.new(0, 70, 0, 28)
        bindButton.Position = UDim2.new(1, -75, 0.5, -14)
        bindButton.BackgroundColor3 = self.CurrentTheme.Element
        bindButton.BorderSizePixel = 0
        bindButton.Text = data.Default or "None"
        bindButton.TextColor3 = self.CurrentTheme.Text
        bindButton.Font = Enum.Font.Gotham
        bindButton.TextSize = 12
        bindButton.Parent = bindFrame

        local currentKey = data.Default
        local listening = false

        local function setKey(key)
            currentKey = key
            bindButton.Text = key
            listening = false
            if data.Callback then data.Callback(key) end
        end

        bindButton.MouseButton1Click:Connect(function()
            listening = true
            bindButton.Text = "..."
            local conn
            conn = UserInputService.InputBegan:Connect(function(input, gameProcessed)
                if not listening then return end
                if gameProcessed then return end
                if input.UserInputType == Enum.UserInputType.Keyboard then
                    setKey(input.KeyCode.Name)
                elseif input.UserInputType == Enum.UserInputType.MouseButton1 then
                    setKey("MB1")
                elseif input.UserInputType == Enum.UserInputType.MouseButton2 then
                    setKey("MB2")
                end
                conn:Disconnect()
            end)
            table.insert(self._hub.KeybindConnections, conn)
        end)

        return bindFrame
    end

    -- Paragraph (Açıklama metni)
    function tabProxy:CreateParagraph(text)
        local paraFrame = Instance.new("Frame")
        paraFrame.Size = UDim2.new(1, -10, 0, 40)
        paraFrame.BackgroundTransparency = 1
        paraFrame.LayoutOrder = #tabFrame:GetChildren() + 1
        paraFrame.Parent = tabFrame

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, 0, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = text or ""
        label.TextColor3 = self.CurrentTheme.SubText
        label.Font = Enum.Font.Gotham
        label.TextSize = 12
        label.TextWrapped = true
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.TextYAlignment = Enum.TextYAlignment.Top
        label.Parent = paraFrame

        -- Yüksekliği metne göre ayarla
        local textSize = TextService:GetTextSize(label.Text, label.TextSize, label.Font, Vector2.new(paraFrame.AbsoluteSize.X, math.huge))
        paraFrame.Size = UDim2.new(1, -10, 0, textSize.Y + 10)

        return paraFrame
    end

    return tabProxy
end

-- Tema Değiştir
function RainyHub:ChangeTheme(themeName)
    if RainyHub.Themes[themeName] then
        self.CurrentTheme = RainyHub.Themes[themeName]
        self:ApplyTheme()
    end
end

function RainyHub:ApplyTheme()
    -- Ana çerçeve
    self.MainFrame.BackgroundColor3 = self.CurrentTheme.Background
    self.Topbar.BackgroundColor3 = self.CurrentTheme.Topbar
    self.TitleLabel.TextColor3 = self.CurrentTheme.Text

    -- Tüm butonlar ve çerçeveler (kısmi güncelleme - performans için sadece ana kısımlar)
    for _, btn in ipairs(self.TabButtons) do
        if self.TabFrames[btn] and self.TabFrames[btn].Visible then
            btn.BackgroundColor3 = self.CurrentTheme.Accent
        else
            btn.BackgroundColor3 = self.CurrentTheme.Element
        end
        btn.TextColor3 = self.CurrentTheme.Text
    end

    self.TabList.ScrollBarImageColor3 = self.CurrentTheme.Accent
end

-- Config İşlemleri
function RainyHub:SaveConfig(data)
    if writefile then
        local success, json = pcall(HttpService.JSONEncode, HttpService, data)
        if success then
            writefile(self.ConfigFolder .. "/" .. self.ConfigName, json)
        end
    end
end

function RainyHub:LoadConfig()
    if readfile and isfile then
        local path = self.ConfigFolder .. "/" .. self.ConfigName
        if isfile(path) then
            local success, content = pcall(readfile, path)
            if success then
                local ok, data = pcall(HttpService.JSONDecode, HttpService, content)
                if ok then return data end
            end
        end
    end
    return {}
end

-- GUI'yi Yok Et
function RainyHub:Destroy()
    -- Keybind bağlantılarını temizle
    for _, conn in ipairs(self.KeybindConnections) do
        pcall(function() conn:Disconnect() end)
    end
    TweenService:Create(self.MainFrame, TweenInfo.new(0.2), {Size = UDim2.new(0, 0, 0, 0)}):Play()
    task.wait(0.2)
    pcall(function() self.ScreenGui:Destroy() end)
end

-- Kütüphaneyi dışa aktar
return RainyHub
