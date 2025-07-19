import torch
import torch.nn.functional as F


class ResizeToCustomAspectRatio:
    """
    Resizes input images based on a specified aspect ratio
    Maintains the original aspect ratio while aligning either the longer or shorter side to the target resolution
    """
    
    ALIGN_MODE_LONGER = "Align Longer Side"
    ALIGN_MODE_SHORTER = "Align Shorter Side"
    
    INTERPOLATION_MODES = {
        "nearest": "nearest",
        "linear": "linear", 
        "bilinear": "bilinear",
        "bicubic": "bicubic",
        "trilinear": "trilinear",
        "area": "area",
        "nearest-exact": "nearest-exact"
    }
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "original_width": ("INT", {
                    "default": 1920,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                    "display": "number"
                }),
                "original_height": ("INT", {
                    "default": 1080,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                    "display": "number"
                }),
                "target_resolution": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                    "display": "number"
                }),
                "align_mode": ([cls.ALIGN_MODE_LONGER, cls.ALIGN_MODE_SHORTER],),
                "interpolation": (list(cls.INTERPOLATION_MODES.keys()), {
                    "default": "bilinear"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "resize_by_aspect"
    CATEGORY = "image/transform"
    
    def resize_by_aspect(self, image, original_width, original_height, target_resolution, align_mode, interpolation):
        # Get current size of input image
        batch_size, current_height, current_width, channels = image.shape
        
        # Calculate original aspect ratio
        original_aspect_ratio = original_width / original_height
        
        # Identify longer and shorter sides
        if original_width >= original_height:
            original_longer = original_width
            original_shorter = original_height
            is_landscape = True
        else:
            original_longer = original_height
            original_shorter = original_width
            is_landscape = False
        
        # Calculate target size
        if align_mode == self.ALIGN_MODE_LONGER:
            # Align longer side to target_resolution
            if is_landscape:
                new_width = target_resolution
                new_height = int(target_resolution / original_aspect_ratio)
            else:
                new_height = target_resolution
                new_width = int(target_resolution * original_aspect_ratio)
        else:
            # Align shorter side to target_resolution
            if is_landscape:
                new_height = target_resolution
                new_width = int(target_resolution * original_aspect_ratio)
            else:
                new_width = target_resolution
                new_height = int(target_resolution / original_aspect_ratio)
        
        # Ensure size is at least 1
        new_width = max(1, new_width)
        new_height = max(1, new_height)
        
        # Resize image
        # PyTorch interpolation expects (batch, channel, height, width) format
        image_permuted = image.permute(0, 3, 1, 2)
        
        # Resize with selected interpolation method
        mode = self.INTERPOLATION_MODES[interpolation]
        
        # antialias is only supported for certain modes
        antialias_modes = ['bilinear', 'bicubic']
        use_antialias = mode in antialias_modes
        
        # align_corners cannot be used with certain modes
        no_align_corners_modes = ['nearest', 'area', 'nearest-exact']
        use_align_corners = False if mode in no_align_corners_modes else False
        
        interpolate_kwargs = {
            'size': (new_height, new_width),
            'mode': mode
        }
        
        if mode not in no_align_corners_modes:
            interpolate_kwargs['align_corners'] = use_align_corners
            
        if use_antialias:
            interpolate_kwargs['antialias'] = True
            
        resized_image = F.interpolate(
            image_permuted,
            **interpolate_kwargs
        )
        
        # Convert back to original format
        resized_image = resized_image.permute(0, 2, 3, 1)
        
        # Clamp values to 0-1 range
        resized_image = torch.clamp(resized_image, 0.0, 1.0)
        
        return (resized_image,)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Always re-execute when inputs change
        return float("nan")


NODE_CLASS_MAPPINGS = {
    "ResizeToCustomAspectRatio": ResizeToCustomAspectRatio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResizeToCustomAspectRatio": "Resize to Custom Aspect Ratio"
}