from flask import Flask, render_template, request, jsonify
from torchvision.transforms.functional import to_pil_image
import torch
from PIL import Image
from torchvision import transforms
from mtlface.face_aligment import face_process as align_faces
from mtlface.modules import MTLFace
import io
import base64

app = Flask(__name__)

# Load the MTLFace model
mtlface = MTLFace().cuda().eval()
mtlface.load_state_dict(torch.load('mtlface_checkpoints.tar'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    # Get the uploaded image from html form 
    uploaded_file = request.files['image'] 
    
    # Process the image
    input_img = Image.open(uploaded_file).convert("RGB")
    aligned_image = align_faces(input_img)

    transform = transforms.Compose([
        transforms.Resize(112),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    input_img = transform(aligned_image).unsqueeze(0).cuda()

    # Perform age invariant face recognition
    with torch.no_grad():
        x_vec, x_age = mtlface.encode(input_img)
        # Perform age synthesis
        bs = input_img.size(0)
        target_labels = torch.arange(7).cuda().unsqueeze(1).repeat(bs, 1).flatten()
        repeat_images = input_img.unsqueeze(1).repeat(1, 7, 1, 1, 1).view(-1, 3, 112, 112)
        outputs = mtlface.aging(repeat_images, target_labels).view(bs, 7, 3, 112, 112)

    #Convert synthesized images to base64 strings
    synthesized_images_b64 = []
    for batch_images in outputs:
        for img in batch_images:
            img_pil = to_pil_image(img.cpu()*0.5+0.5)
            img_buffer = io.BytesIO()
            img_pil.save(img_buffer, format='PNG')
            img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            synthesized_images_b64.append(img_str)
    
    # Round estimated age to nearest year
    rounded_age = round(x_age.item())

    # Return the synthesized images, rounded age, and uploaded image as JSON response
    response_data = {
        'synthesized_images': synthesized_images_b64,
        'rounded_age': rounded_age
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
