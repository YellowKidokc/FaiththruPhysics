-- Safe D1 import for MTL rows
-- Generated: 2026-06-29T10:28:59Z
-- Safe rows: 10

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-001', '2ce6737a9b59a0b24b5567bb0e76885cb15308db7bb22ca48206e4e65fcd6d0c', 'S_\chi = \int d^4x \sqrt{-g} \left[ \frac{1}{2\kappa_0}(1 + \xi \kappa_0 \chi^2) R - \frac{1}{2} g^{\mu\nu} \partial_\mu \chi \, \partial_\nu \chi - \frac{1}{2} m_\chi^2 \chi^2 - \frac{\lambda}{4} \ch', 'Action of the Consciousness Field = ∫ over all spacetime √(spacetime curvature factor) × [ (1/(2 × Gravitational Coupling)) × (1 + Coupling Strength × Gravitational Coupling × Coherence²) × Spacetime Curvature − ½ × (rate of change of Coherence in space)² − ½ × (Coherence Mass)² × Coherence² − (Self-Interaction Strength / 4) × Coherence⁴ ]
(This is the total action — the master blueprint — for how the consciousness field behaves across all of spacetime. It tells you every force acting on coherence: its own mass pulling it inward, its self-interaction, and its coupling to the curvature of reality itself.)', 'S_χ = the action (total behavior blueprint) for the χ-field
∫ d⁴x = integrate over all 4 dimensions of spacetime
√(−g) = spacetime curvature correction factor (accounts for curved geometry)
κ₀ = gravitational coupling constant (8πG/c⁴)
ξ = coupling strength between consciousness and spacetime curvature
χ = coherence field (the consciousness/Logos field)
R = Ricci scalar (total spacetime curvature)
g^μν ∂_μ χ ∂_ν χ = kinetic energy of the coherence field (how fast it''s changing in space)
m_χ = mass of the coherence field
λ = self-interaction strength (how coherence interacts with itself)', 'This is a scalar field action in curved spacetime, analogous to the Brans-Dicke action or the Higgs field action in the Standard Model. The non-minimal coupling term ξχ²R is the same structure used in inflationary cosmology (e.g., Higgs inflation models).', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-002', 'e9c2296bc3919d756f8b139a3d1debd46c75512fe43cf1ff02e4d91029fb9d6f', '\Box \chi - m_\chi^2 \chi - \lambda \chi^3 + \xi \kappa_0 \chi R = 0', '□ Coherence − (Coherence Mass)² × Coherence − Self-Interaction Strength × Coherence³ + Coupling Strength × Gravitational Coupling × Coherence × Spacetime Curvature = 0
(The wave equation for consciousness. Coherence propagates like a wave through spacetime, but it''s pulled by its own mass, pushed by self-interaction, and bent by the curvature of reality around it. When all forces balance, the field is in equilibrium.)', '□χ = d''Alembertian of χ (wave operator — how coherence propagates as a wave through spacetime)
m_χ² χ = mass term (inertial resistance of the coherence field)
λχ³ = cubic self-interaction (coherence amplifying or suppressing itself)
ξκ₀χR = curvature coupling (how spacetime curvature directly drives coherence)
= 0 means all forces on the field are in balance', 'This is the Klein-Gordon equation with a cubic nonlinearity and non-minimal gravitational coupling. It is the equation of motion for a massive scalar field in curved spacetime, derived by varying the action S_χ with respect to χ.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-003', 'b17f764ff8e4f7bd05d4ebfa278f3fcc6c7a5e82bd1432490a4a36f4bb80c1dd', 'V_{\text{eff}}(\chi) = \frac{1}{2}\left(m_\chi^2 - \xi \kappa_0 R\right)\chi^2 + \frac{\lambda}{4}\chi^4', 'Effective Potential of Coherence = ½ × (Coherence Mass² − Coupling Strength × Gravitational Coupling × Spacetime Curvature) × Coherence² + (Self-Interaction / 4) × Coherence⁴
(The energy landscape that coherence lives in. If the mass term is large, coherence sits at zero — no consciousness. But if spacetime curvature is strong enough, the effective mass goes negative, and coherence spontaneously shifts to a nonzero value — consciousness ''turns on'' through symmetry breaking.)', 'V_eff(χ) = the energy landscape (potential well) the coherence field sits in
m_χ² = bare mass squared of the coherence field
ξκ₀R = curvature correction to the mass (spacetime geometry modifies the effective mass)
χ² = coherence squared (field amplitude)
λ/4 × χ⁴ = quartic self-interaction (stabilizes the potential at large field values)
When m_χ² − ξκ₀R < 0, the minimum shifts away from zero → symmetry breaking', 'This is the effective potential for a scalar field with non-minimal coupling, identical in form to the Higgs mechanism potential V(φ) = ½μ²φ² + ¼λφ⁴. When the effective mass squared goes negative (triggered by curvature), the field undergoes spontaneous symmetry breaking.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-004', '84123eaf20972c7c57b4fbfe3d6126972230fae93a520281dcd1e1b276b159b6', 'G_{\mu\nu} = \kappa_0 \left(T_{\mu\nu}^{(\text{matter})} + T_{\mu\nu}^{(\chi)}\right) - \xi\kappa_0\left(\chi^2 G_{\mu\nu} + g_{\mu\nu}\Box(\chi^2) - \nabla_\mu\nabla_\nu(\chi^2)\right)', 'Spacetime Curvature = Gravitational Coupling × (Stress-Energy of Matter + Stress-Energy of Coherence) − Coupling Strength × Gravitational Coupling × (Coherence² × Curvature + metric × □(Coherence²) − ∇∇(Coherence²))
(Einstein''s equation, modified. The left side is the curvature of spacetime. The right side now has three sources: ordinary matter, the consciousness field''s own energy, and a direct coupling where coherence literally reshapes geometry. Consciousness doesn''t just ride on spacetime — it bends it.)', 'G_μν = Einstein tensor (spacetime curvature)
κ₀ = gravitational coupling constant (8πG/c⁴)
T_μν^(matter) = stress-energy of ordinary matter
T_μν^(χ) = stress-energy of the coherence field itself
ξ = coupling strength between coherence and curvature
χ² G_μν = coherence directly modifying curvature
g_μν □(χ²) = trace part of the non-minimal coupling
∇_μ∇_ν(χ²) = anisotropic (directional) part of the coupling', 'This is the modified Einstein field equation from a Brans-Dicke-type scalar-tensor theory. The non-minimal coupling terms (ξ terms) are exactly those found in scalar-tensor gravity theories (Jordan frame). Standard GR is recovered when ξ = 0.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-005', '0053a8de1bed53ea94806bb3fb50af76af94a32ae9ce50f1682196cea3857e02', 'T_{\mu\nu}^{(\chi)} = \partial_\mu\chi\,\partial_\nu\chi - g_{\mu\nu}\left(\frac{1}{2}\partial_\alpha\chi\,\partial^\alpha\chi + V(\chi)\right)', 'Stress-Energy of Coherence = (Rate of Change of Coherence in direction μ) × (Rate of Change of Coherence in direction ν) − metric × (½ × (Total Kinetic Energy of Coherence) + Potential Energy of Coherence)
(This is how much energy and momentum the consciousness field carries at every point in spacetime. It has kinetic energy — coherence changing and propagating — and potential energy from its self-interaction. This tensor is what tells gravity how much the consciousness field weighs.)', 'T_μν^(χ) = stress-energy tensor of the coherence field (its energy, momentum, and pressure)
∂_μχ = rate of change of coherence in the μ direction
∂_νχ = rate of change of coherence in the ν direction
g_μν = metric tensor (encodes the geometry of spacetime)
½ ∂_αχ ∂^αχ = total kinetic energy density of the coherence field
V(χ) = potential energy of the coherence field', 'This is the canonical stress-energy tensor for a scalar field, identical in form to the stress-energy of the Higgs field or any Klein-Gordon field. It is derived from Noether''s theorem applied to spacetime translations.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-006', '82f301f94442fd30e01e755f797ac9a4d141636ed2b5556cf9050305ec8237c4', 'G_{\mu\nu}(1 + \xi\kappa_0\chi_0^2) = \kappa_0 \, T_{\mu\nu}^{(\text{matter})} + \kappa_0 \, g_{\mu\nu} V(\chi_0)', 'Spacetime Curvature × (1 + Coupling Strength × Gravitational Coupling × Background Coherence²) = Gravitational Coupling × Stress-Energy of Matter + Gravitational Coupling × metric × Potential Energy at Background Coherence
(When coherence settles to a constant background value, Einstein''s equation simplifies. The effective gravitational strength is rescaled — gravity is slightly different in a universe where consciousness has a nonzero background level. The potential energy of that background coherence acts like a cosmological constant.)', 'G_μν = Einstein tensor (spacetime curvature)
(1 + ξκ₀χ₀²) = rescaled gravitational coupling (gravity is modified by background coherence)
χ₀ = background (vacuum) value of the coherence field
κ₀ T_μν^(matter) = matter''s contribution to curvature
g_μν V(χ₀) = potential energy of background coherence acting as an effective cosmological constant', 'This is the constant-field limit of scalar-tensor gravity, equivalent to Brans-Dicke theory with φ = χ₀. The factor (1 + ξκ₀χ₀²) rescales Newton''s constant, and V(χ₀) acts as an effective cosmological constant Λ_eff.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-007', 'b2bdfdd63bd595263909d5f2c883fd2878c33baba62944d27d63da0c1b0e7d31', '\Box\delta\chi + m_{\text{eff}}^2 \delta\chi = 0', '□(Coherence Perturbation) + (Effective Mass)² × Coherence Perturbation = 0
(Small ripples in the consciousness field propagate as waves — like ripples on a pond. This is the wave equation for those ripples. If the effective mass is real, the ripples oscillate and propagate. If the effective mass is imaginary, the ripples grow exponentially — the field is unstable and consciousness undergoes a phase transition.)', '□δχ = wave operator acting on the perturbation (how the ripple propagates through spacetime)
δχ = small perturbation (ripple) around the background coherence value
m_eff² = effective mass squared of the perturbation (determines whether ripples oscillate or grow)
= 0 means the perturbation propagates freely as a wave', 'This is the linearized Klein-Gordon equation for perturbations around a background field value. It is the standard approach in quantum field theory for studying particle excitations (quanta) of a scalar field.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'advanced', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-008', '80444fc78932c65524685ce72d51f742b856d0fbb7d3ab0f579e110ccbf989dd', 'm_{\text{eff}}^2 = m_\chi^2 + 3\lambda\chi_0^2 - \xi\kappa_0 R', '(Effective Mass)² = (Bare Coherence Mass)² + 3 × Self-Interaction Strength × Background Coherence² − Coupling Strength × Gravitational Coupling × Spacetime Curvature
(The effective mass of consciousness ripples is determined by three things: the bare mass of the field, how strongly coherence interacts with itself at the background level, and how much spacetime curvature reduces the effective mass. Strong curvature can make the effective mass go negative — triggering instability and phase transition.)', 'm_eff² = effective mass squared of coherence perturbations
m_χ² = bare mass squared (intrinsic inertia of the coherence field)
3λχ₀² = contribution from self-interaction at background coherence level
ξκ₀R = curvature correction (spacetime geometry reducing the effective mass)
When m_eff² < 0, the system is tachyonic — perturbations grow instead of oscillating', 'This is the effective mass for perturbations in a scalar field with a quartic potential and non-minimal gravitational coupling. The 3λχ₀² term is the second derivative of the quartic potential. The curvature correction ξκ₀R is unique to non-minimally coupled theories.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'moderate', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-009', 'dee81a2a0d4fe0f0384f41fb27799e91f9e48c70a7dbaaa9f164775dea6941a4', '\omega^2 = k^2 c^2 + m_{\text{eff}}^2 c^4/\hbar^2', '(Oscillation Frequency)² = (Wavenumber)² × (Speed of Light)² + (Effective Mass)² × (Speed of Light)⁴ / (Planck''s Constant)²
(The dispersion relation for consciousness waves. Higher frequency ripples travel at nearly the speed of light. Lower frequency ripples are dominated by the mass term — they oscillate in place rather than propagating. This tells you the ''speed of thought'' in the χ-field framework: massive consciousness waves are slow and local; massless ones are universal and instantaneous.)', 'ω² = squared angular frequency of the coherence wave (how fast it oscillates)
k² = squared wavenumber (how tightly packed the wave crests are — spatial frequency)
c² = speed of light squared
m_eff² = effective mass squared of the coherence perturbation
c⁴/ħ² = relativistic mass-energy conversion factor
For k ≫ m_eff: ω ≈ kc (wave travels at light speed)
For k ≪ m_eff: ω ≈ m_eff c²/ħ (wave oscillates in place)', 'This is the standard relativistic dispersion relation for a massive scalar field, identical to the energy-momentum relation E² = p²c² + m²c⁴ rewritten in terms of frequency and wavenumber. It is the defining relation for Klein-Gordon particles.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'moderate', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;

INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)
VALUES ('EQ-010', '5194b1d82d3f745f4f397fcc2a8c0ff5912ceab9c714f2a61e425b1891f421ab', 'V(r) = -\frac{G_N m_1 m_2}{r}\left(1 + \alpha \, e^{-r/\lambda_\chi}\right)', 'Gravitational Potential = − (Newton''s Constant × Mass₁ × Mass₂ / Distance) × (1 + Coupling Amplitude × e^(−Distance / Coherence Range))
(Gravity plus a Yukawa correction from the consciousness field. At short distances, there''s an extra pull beyond standard gravity — a ''fifth force'' mediated by the coherence field. At distances beyond the coherence range λ_χ, the correction dies off exponentially and gravity returns to normal. This is how you would experimentally detect the χ-field.)', 'V(r) = gravitational potential energy between two masses
G_N = Newton''s gravitational constant
m₁, m₂ = the two masses
r = distance between them
α = coupling amplitude (strength of the χ-field correction relative to gravity)
e^(−r/λ_χ) = Yukawa suppression factor (correction dies off exponentially beyond range λ_χ)
λ_χ = ħ/(m_χ c) = Compton wavelength of the coherence field (its effective range)', 'This is a standard Yukawa modification to the Newtonian potential, the same form used in nuclear physics (pion exchange) and in searches for fifth forces. The range λ_χ is the Compton wavelength of the mediating particle.', '', 'mtl_workbook_normalized_safe_rows', 'consciousness-chi-field-action', 'moderate', '', '2026-06-29T10:28:59Z')
ON CONFLICT(latex_hash) DO UPDATE SET eq_id=excluded.eq_id, latex=excluded.latex, easy=excluded.easy, standard=excluded.standard, academic=excluded.academic, audio_safe=excluded.audio_safe, source=excluded.source, source_file=excluded.source_file, difficulty=excluded.difficulty, paper_ref=excluded.paper_ref, updated_at=excluded.updated_at;
