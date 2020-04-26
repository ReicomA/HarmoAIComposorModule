
# Copyright SweetCase Project, Re_Coma(Ha Jeong Hyun). All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music.protobuf import generator_pb2
from magenta.music.protobuf import music_pb2
import magenta.music as mm

class DeepLearningProcessor:
    """ TODO GPU 조절할 코드 작성 필요 """
    def __init__(self, modelRoot, noteSize, resultFileName):

        # TODO 전처리 필요
        self.modelRoot = modelRoot
        self.noteSize = noteSize
        self.resultFileName = resultFileName

    def makeModel(self):
        """ EXAMPLE """
        bundle = sequence_generator_bundle.read_bundle_file(self.modelRoot)
        generator_map = melody_rnn_sequence_generator.get_generator_map()
        self.model = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
        self.model.initialize()

    def makeInputSequence(self):
        # TODO 랜덤으로 돌려야됨
        input_sequence = music_pb2.NoteSequence()
        input_sequence.notes.add(pitch=72, start_time=0.0, end_time=0.5, velocity=80)
        input_sequence.total_time = 8
        input_sequence.tempos.add(qpm=60)

        return input_sequence

    def setConfigure(self, input_sequence):

        num_steps = 20
        temperature = 1.2
        last_end_time = (max(n.end_time for n in input_sequence.notes)
                        if input_sequence.notes else 0)
        
        qpm = input_sequence.tempos[0].qpm
        seconds_per_step = 60.0/qpm/self.model.steps_per_quarter
        total_seconds = num_steps * seconds_per_step

        generator_options = generator_pb2.GeneratorOptions()
        generator_options.args['temperature'].float_value = temperature
        generate_section = generator_options.generate_sections.add(
            start_time=last_end_time + seconds_per_step,
            end_time=total_seconds)
        return generator_options
    
    def generate(self, input_sequence, options):
        return self.model.generate(input_sequence, options)

    def makeFile(self, result):
        mm.sequence_proto_to_midi_file(result, self.resultFileName)
