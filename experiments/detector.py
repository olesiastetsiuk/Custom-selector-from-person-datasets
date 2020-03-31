import numpy as np
import tensorflow as tf


class Detector:
    def __init__(self, model_path, gpu_memory_fraction=0.4, visible_device_list='0'):

        with tf.gfile.GFile(model_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        graph = tf.Graph()
        with graph.as_default():
            tf.import_graph_def(graph_def, name='import')

        self.input_image = graph.get_tensor_by_name('import/image_tensor:0')
        self.output_ops = {
            'boxes': graph.get_tensor_by_name('import/detection_boxes:0'),
            'scores': graph.get_tensor_by_name('import/detection_scores:0'),
            'labels': graph.get_tensor_by_name('import/detection_classes:0'),
            'num_boxes': graph.get_tensor_by_name('import/num_detections:0'),
        }

        gpu_options = tf.GPUOptions(
            per_process_gpu_memory_fraction=gpu_memory_fraction,
            visible_device_list=visible_device_list
        )
        config_proto = tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False)
        self.sess = tf.Session(graph=graph, config=config_proto)

    def __call__(self, image, score_threshold=0.5):

        feed_dict = {self.input_image: np.expand_dims(image, 0)}
        result = self.sess.run(self.output_ops, feed_dict)

        num_boxes = int(result['num_boxes'][0])
        boxes = result['boxes'][0][:num_boxes]
        scores = result['scores'][0][:num_boxes]
        labels = result['labels'][0][:num_boxes].astype(int)

        to_keep = scores > score_threshold
        boxes = boxes[to_keep]
        scores = scores[to_keep]
        labels = labels[to_keep]

        return boxes, scores, labels