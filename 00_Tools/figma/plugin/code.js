figma.showUI(__html__, { width: 340, height: 280 });

function log(msg) {
  figma.ui.postMessage({ type: 'LOG', message: msg });
}

async function handleCommands(commands) {
  // 基本フォントの事前読み込み
  const fontList = [
    { family: "Inter", style: "Regular" },
    { family: "Inter", style: "Bold" },
    { family: "Noto Sans JP", style: "Regular" },
    { family: "Noto Sans JP", style: "Bold" }
  ];

  for (const font of fontList) {
    try { await figma.loadFontAsync(font); } catch (e) {}
  }

  const nodeMap = new Map();

  for (const cmd of commands) {
    try {
      let createdNode = null;

      if (cmd.action === "clear_canvas") {
        const selection = figma.currentPage.children.slice();
        for (const node of selection) { node.remove(); }
        log("キャンバスをクリアしました。");
        continue;
      }

      if (cmd.action === "create_frame") {
        const frame = figma.createFrame();
        frame.name = cmd.name || "Frame";
        frame.resize(cmd.width !== undefined ? cmd.width : 100, cmd.height !== undefined ? cmd.height : 100);

        if (cmd.bg) frame.fills = [{ type: 'SOLID', color: cmd.bg }];
        else if (cmd.bg === null) frame.fills = [];

        if (cmd.borderColor) {
          frame.strokes = [{ type: 'SOLID', color: cmd.borderColor }];
          frame.strokeWeight = cmd.borderWidth || 1;
        }

        if (cmd.cornerRadius !== undefined) frame.cornerRadius = cmd.cornerRadius;
        frame.clipsContent = cmd.clipsContent !== undefined ? cmd.clipsContent : false;

        if (cmd.layoutMode && (cmd.layoutMode === "HORIZONTAL" || cmd.layoutMode === "VERTICAL")) {
          frame.layoutMode = cmd.layoutMode;
          if (cmd.primaryAxisSizingMode) frame.primaryAxisSizingMode = cmd.primaryAxisSizingMode;
          if (cmd.counterAxisSizingMode) frame.counterAxisSizingMode = cmd.counterAxisSizingMode;
          if (cmd.paddingLeft !== undefined) frame.paddingLeft = cmd.paddingLeft;
          if (cmd.paddingRight !== undefined) frame.paddingRight = cmd.paddingRight;
          if (cmd.paddingTop !== undefined) frame.paddingTop = cmd.paddingTop;
          if (cmd.paddingBottom !== undefined) frame.paddingBottom = cmd.paddingBottom;
          if (cmd.itemSpacing !== undefined) frame.itemSpacing = cmd.itemSpacing;
          if (cmd.primaryAxisAlignItems) frame.primaryAxisAlignItems = cmd.primaryAxisAlignItems;
          if (cmd.counterAxisAlignItems) frame.counterAxisAlignItems = cmd.counterAxisAlignItems;
        }

        createdNode = frame;

      } else if (cmd.action === "create_text") {
        const text = figma.createText();
        const fontFamily = cmd.fontFamily || "Inter";
        const fontStyle = cmd.fontStyle || "Regular";
        
        try {
          await figma.loadFontAsync({ family: fontFamily, style: fontStyle });
          text.fontName = { family: fontFamily, style: fontStyle };
        } catch (e) {
          await figma.loadFontAsync({ family: "Inter", style: "Regular" });
          text.fontName = { family: "Inter", style: "Regular" };
        }

        text.name = cmd.name || "Text";
        text.characters = cmd.text !== undefined ? String(cmd.text) : "";
        text.fontSize = cmd.fontSize || 14;

        if (cmd.color) text.fills = [{ type: 'SOLID', color: cmd.color }];
        if (cmd.textAlignHorizontal) text.textAlignHorizontal = cmd.textAlignHorizontal;

        if (cmd.width && cmd.width > 0) {
          text.textAutoResize = cmd.textAutoResize || "HEIGHT";
          text.resize(cmd.width, text.height || 20);
        } else {
          text.textAutoResize = cmd.textAutoResize || "WIDTH_AND_HEIGHT";
        }

        createdNode = text;

      } else if (cmd.action === "create_rect") {
        const rect = figma.createRectangle();
        rect.name = cmd.name || "Rectangle";
        rect.resize(cmd.width || 100, cmd.height || 100);
        
        if (cmd.color) rect.fills = [{ type: 'SOLID', color: cmd.color }];
        if (cmd.borderColor) {
          rect.strokes = [{ type: 'SOLID', color: cmd.borderColor }];
          rect.strokeWeight = cmd.borderWidth || 1;
        }
        if (cmd.cornerRadius) rect.cornerRadius = cmd.cornerRadius;

        createdNode = rect;
      }

      if (createdNode) {
        if (cmd.key) nodeMap.set(cmd.key, createdNode);

        let parentNode = null;
        if (cmd.parentKey && nodeMap.has(cmd.parentKey)) {
          parentNode = nodeMap.get(cmd.parentKey);
        } else if (cmd.parentId) {
          parentNode = figma.getNodeById(cmd.parentId);
        }

        if (parentNode && parentNode.appendChild) {
          parentNode.appendChild(createdNode);
        }

        if (cmd.x !== undefined) createdNode.x = cmd.x;
        if (cmd.y !== undefined) createdNode.y = cmd.y;

        if (parentNode && parentNode.layoutMode && parentNode.layoutMode !== "NONE") {
          if (cmd.layoutAlign) createdNode.layoutAlign = cmd.layoutAlign;
          if (cmd.layoutGrow !== undefined) createdNode.layoutGrow = cmd.layoutGrow;
        }

        log(`作成: ${createdNode.name}`);
      }

    } catch (err) {
      log(`エラー (${cmd.action}): ${err.message}`);
    }
  }

  if (nodeMap.has("artboard") || nodeMap.has("root")) {
    const rootNode = nodeMap.get("artboard") || nodeMap.get("root");
    figma.currentPage.selection = [rootNode];
    figma.viewport.scrollAndZoomIntoView([rootNode]);
  }

  log("全描画コマンドの処理が完了しました！");
}

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'EXEC_COMMANDS') {
    await handleCommands(msg.commands);
  }
};


