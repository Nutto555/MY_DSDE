class Animation {
    constructor(img_id, slider_id, frames) {
        this.img = document.getElementById(img_id);
        this.slider = document.getElementById(slider_id);
        this.frames = frames;
        this.current_frame = 0;
        this.interval = null;
        this.direction = 1;  // 1 for forward, -1 for reverse

        this.slider.max = this.frames.length - 1;
        this.slider.value = this.current_frame;
        this.slider.addEventListener('input', () => this.set_frame(parseInt(this.slider.value)));
        
        this.set_frame(this.current_frame);
    }

    set_frame(frame) {
        if (frame >= 0 && frame < this.frames.length) {
            this.current_frame = frame;
            this.img.src = this.frames[frame];
            this.slider.value = frame;
        }
    }

    play_animation() {
        this.pause_animation();
        this.interval = setInterval(() => {
            let newFrame = this.current_frame + this.direction;
            if (newFrame >= this.frames.length || newFrame < 0) {
                this.direction *= -1;
                newFrame = this.current_frame + this.direction;
            }
            this.set_frame(newFrame);
        }, 100);  // Adjust timing as needed
    }

    pause_animation() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }

    first_frame() {
        this.set_frame(0);
    }

    last_frame() {
        this.set_frame(this.frames.length - 1);
    }

    next_frame() {
        this.set_frame(this.current_frame + 1);
    }

    previous_frame() {
        this.set_frame(this.current_frame - 1);
    }

    slower() {
        // Increase interval for slower animation
        clearInterval(this.interval);
        this.play_animation();
    }

    faster() {
        // Decrease interval for faster animation
        clearInterval(this.interval);
        this.play_animation();
    }

    reverse_animation() {
        this.direction *= -1;
        this.play_animation();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const frames = [];
    for (let i = 0; i <= 590; i++) {
        let frameNumber = String(i).padStart(7, '0');
        frames.push(`bcr_race_frames/frame${frameNumber}.png`);
    }
    window.animation = new Animation('animation_img', 'frame_slider', frames);
});
