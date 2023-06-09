# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# Standard library imports
from typing import List

# Third-party imports
import torch
import torch.nn as nn
from torch import Tensor

# First-party imports
from pts.core.component import validated
from pts.modules.block.mlp import MLP


class Seq2SeqDecoder(nn.Module):
    """
    Abstract class for the Decoder block in sequence-to-sequence models.
    """

    @validated()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # noinspection PyMethodOverriding
    def forward(
        self, dynamic_input: Tensor, static_input: Tensor
    ) -> None:
        """
        Abstract function definition of the forward.

        Parameters
        ----------
        dynamic_input
            dynamic_features, shape (batch_size, sequence_length, num_features)
            or (N, T, C)

        static_input
            static features, shape (batch_size, num_features) or (N, C)

        """
        pass

'''
class ForkingMLPDecoder(Seq2SeqDecoder):
    """
    Multilayer perceptron decoder for sequence-to-sequence models.

    See [WTN+17]_ for details.

    Parameters
    ----------
    dec_len
        length of the decoder (usually the number of forecasted time steps).

    final_dim
        dimensionality of the output per time step (number of predicted
        quantiles).

    hidden_dimension_sequence
        number of hidden units for each MLP layer.
    """

    @validated()
    def __init__(
        self,
        dec_len: int,
        final_dim: int,
        hidden_dimension_sequence: List[int] = list([]),
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.dec_len = dec_len
        self.final_dims = final_dim

        
        self.model = nn.Sequential()

        for layer_no, layer_dim in enumerate(hidden_dimension_sequence):
            layer = nn.Linear(
                dec_len * layer_dim,
                flatten=False,
                activation="relu",
                prefix=f"mlp_{layer_no:#02d}'_",
            )
            self.model.add(layer)

        layer = nn.Linear(
            dec_len * final_dim,
            flatten=False,
            activation="softrelu",
            prefix=f"mlp_{len(hidden_dimension_sequence):#02d}'_",
        )
        self.model.add(layer)

    def forward(
        self, dynamic_input: Tensor, static_input: Tensor = None
    ) -> Tensor:
        """
        ForkingMLPDecoder forward call.

        Parameters
        ----------

        dynamic_input
            dynamic_features, shape (batch_size, sequence_length, num_features)
            or (N, T, C).

        static_input
            not used in this decoder.

        Returns
        -------
        Tensor
            mlp output, shape (0, 0, dec_len, final_dims).

        """
        mlp_output = self.model(dynamic_input)
        mlp_output = mlp_output.reshape(
            shape=(0, 0, self.dec_len, self.final_dims)
        )
        return mlp_output
'''

class OneShotDecoder(Seq2SeqDecoder):
    """
    OneShotDecoder.

    Parameters
    ----------
    decoder_length
        length of the decoder (number of time steps)
    layer_sizes
        dimensions of the hidden layers
    static_outputs_per_time_step
        number of outputs per time step
    """

    @validated()
    def __init__(
        self,
        input_size: int,
        decoder_length: int,
        layer_sizes: List[int],
        static_outputs_per_time_step: int,
    ) -> None:
        super().__init__()
        self.decoder_length = decoder_length
        self.static_outputs_per_time_step = static_outputs_per_time_step
    
        self.expander = nn.Linear(
            input_size, 
            decoder_length * static_outputs_per_time_step
        )

        input_size = 4 + static_outputs_per_time_step #TODO: fix hard coded dimension for covariates
        self.mlp = MLP(input_size, layer_sizes)

    def forward(
        self,
        static_input: Tensor,  # (batch_size, static_input_dim)
        dynamic_input: Tensor,  # (batch_size,
    ) -> Tensor:
        """
        OneShotDecoder forward call

        Parameters
        ----------
        static_input
            static features, shape (batch_size, num_features) or (N, C)

        dynamic_input
            dynamic_features, shape (batch_size, sequence_length, num_features)
            or (N, T, C)
        Returns
        -------
        Tensor
            mlp output, shape (batch_size, dec_len, size of last layer)
        """
        static_input_tile = self.expander(static_input).reshape(
            (-1, self.decoder_length, self.static_outputs_per_time_step)
        )
        combined_input = torch.cat([dynamic_input, static_input_tile], dim=2)

        out = self.mlp(combined_input)  # (N, T, layer_sizes[-1])
        return out
