# ComfyUI Custom Aspect Resize

画像品質を保ちながらカスタムアスペクト比にリサイズするComfyUI用カスタムノードです。

## 機能

- カスタムアスペクト比（縦横比）に基づいた画像リサイズ
- 長辺または短辺を目標解像度に合わせる選択が可能
- 複数の補間方法が利用可能：
  - nearest
  - linear
  - bilinear (デフォルト)
  - bicubic
  - trilinear
  - area
  - nearest-exact

## インストール

1. このリポジトリをComfyUIのcustom_nodesフォルダにクローンします：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/comfyui-custom-aspect-resize.git
```

2. ComfyUIを再起動します

## 使用方法

ノードは「image/transform」カテゴリ内に「Resize to Custom Aspect Ratio」として表示されます。

### パラメータ

- **image**: リサイズする入力画像
- **original_width**: 目標アスペクト比の幅 (デフォルト: 1920)
- **original_height**: 目標アスペクト比の高さ (デフォルト: 1080)
- **target_resolution**: 目標解像度（ピクセル） (デフォルト: 1024)
- **align_mode**: 長辺または短辺のどちらを目標解像度に合わせるかを選択
- **interpolation**: リサイズ用の補間方法 (デフォルト: bilinear)

### 使用例1

4:3の画像を16:9のアスペクト比で長辺1024pxにリサイズする場合：
- original_width: 1920
- original_height: 1080
- target_resolution: 1024
- align_mode: "Align Longer Side"

### 使用例2